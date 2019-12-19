#!/usr/bin/env python3

"""
Copyright 2017 3devo (www.3devo.eu)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import argparse
import subprocess
import sortedcontainers
from intelhex import IntelHex
from collections import namedtuple
from elftools.elf.elffile import ELFFile

import dwarf

cppfilt = 'c++filt'

CallInfo = namedtuple('CallInfo', ['mnemonic', 'call_addr', 'callee_addr'])

def demangle(name):
  """ Demangle the given name """
  return subprocess.check_output([cppfilt, name]).decode('utf8').strip()

def address_to_containing_function(symdict, address):
  """
  Convert an instruction address to the demangled name of the function
  that contains the instruction.
  """
  candidate_index = symdict.bisect(address)
  if candidate_index == 0:
    # Address is before first function
    return 'unknown function'
  # -1 to get the symbol that starts *before* the given address
  candidate = symdict[symdict.keys()[candidate_index - 1]]

  start = candidate['st_value']
  end = start + candidate['st_size']

  if start <= address < end:
    return demangle(candidate.name)
  return 'unknown function'

def address_to_function(symdict, address):
  """
  Convert a function address to the demangled name of that function.
  """
  sym = symdict.get(address, None)
  if sym:
    return demangle(sym.name)
  else:
    return 'unknown function at 0x{:06x}'.format(address)

def address_to_location(dwarf_info, addr):
  """
  Convert an instruction address to the filename and number containing
  it, or None if no info was found.
  """
  path, line = dwarf.decode_file_line(dwarf_info, addr)
  if path and line:
    return "{}:{}".format(path.decode('utf8'), line)
  else:
    return None

def process_symtab(elf, arch):
  """
  Yields a sorted dictionary containing the function symbols in the
  .text section, indexed by their starting address.
  """
  symtab = elf.get_section_by_name('.symtab')
  result = sortedcontainers.SortedDict()

  for sym in symtab.iter_symbols():
    if (sym['st_info']['type'] == 'STT_FUNC'):
      if sym['st_size'] <= 0:
        print("Skipping zero-size function: " + demangle(sym.name))
        continue

      if sym['st_shndx'] == 0:
        print("Skipping undefined function: " + demangle(sym.name))
        continue

      section = elf.get_section(sym['st_shndx']).name
      if section != '.text':
        print("Skipping function in section other than .text: {} in {}".format(section, demangle(sym.name)))
        continue

      addr = arch.sym_to_addr(sym)

      result[addr] = sym
  return result

def generate_frame(symdict, dwarf_info, call):
  caller = address_to_containing_function(symdict, call.call_addr)
  sys.stdout.write("0x{:06x}: {} in {}".format(call.call_addr, call.mnemonic, caller))

  # TODO: This is fairly slow
  location = address_to_location(dwarf_info, call.call_addr)
  if location:
    sys.stdout.write(" at {}".format(location))

  if call.callee_addr:
    callee = address_to_function(symdict, call.callee_addr)
    sys.stdout.write(" called {}".format(callee))

  sys.stdout.write("\n")

def generate_stacktrace(elf, memory, arch, isr_ret):
  """
  Generate a stacktrace on stdout from looking at the given memory dump
  and elf file.
  """
  dwarf_info = elf.get_dwarf_info()
  symdict = process_symtab(elf, arch)
  addrlen = arch.get_addrlen()

  # All call instructions in the program
  callsites = arch.find_callsites(elf, symdict)

  print("Stacktrace follows (most recent call first)")

  if isr_ret:
    isr_call = CallInfo(mnemonic='interrupt', call_addr=isr_ret, callee_addr=None)
    generate_frame(symdict, dwarf_info, isr_call)

  # Find all addrlen-sized pointers in the stack that match a call
  # instruction (e.g. are likely a return address on the stack)
  addresses = memory.addresses()
  for addr in addresses:
    if all(addr + i in addresses for i in range(addrlen)):
      ptr = arch.decode_ptr(memory.tobinstr(start=addr, size=addrlen))
      if ptr in callsites:
        generate_frame(symdict, dwarf_info, callsites[ptr])

def main():
  parser = argparse.ArgumentParser(description = 'Analyze AVR memory dumps')
  parser.add_argument('--isr-return', help='ISR return (byte) address to prepend to the trace', metavar='0x123', type=lambda x: int(x, 0))
  parser.add_argument('--elf', help='Compiled elf file')
  parser.add_argument('--cppfilt', help='Path to c++filt command')
  parser.add_argument('memory', help='Memory dump file')
  args = parser.parse_args()

  # Store cppfilt option
  global cppfilt
  if args.cppfilt:
    cppfilt = args.cppfilt

  # Read elf file if specified
  elf = None
  if args.elf:
    # Note that file is kept open, ELFFile reads from it on the fly.
    elf = ELFFile(open(args.elf, 'rb'))

    if elf['e_machine'] == 'EM_AVR':
      import avr
      arch = avr.ArchAvr(elf)
    elif elf['e_machine'] == 'EM_ARM':
      import arm
      arch = arm.ArchArm(elf)
    else:
      sys.stderr.write("Unsupported elf file architecture (machine id: {}, flags: 0x{:X})\n".format(elf['e_machine'], elf['e_flags']))
      sys.exit(1)

  # Read memory file
  memory = IntelHex(args.memory)

  if elf:
    generate_stacktrace(elf, memory, arch, args.isr_return)
  else:
    print("Need elf file to generate stack trace")

main()
