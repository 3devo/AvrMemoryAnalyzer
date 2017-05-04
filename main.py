#!/usr/bin/env python3

import sys
import argparse
import subprocess
import sortedcontainers
from intelhex import IntelHex
from elftools.elf.elffile import ELFFile

import avr
import dwarf

cppfilt = 'c++filt'

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
  candidate = symdict[symdict.iloc[candidate_index - 1]]

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
    return 'unknown function'

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

def process_symtab(elf):
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

      result[sym['st_value']] = sym
  return result

def find_callsites(elf, symdict):
  """
  Look through all code in the .text section and identify call
  instructions. Returns a dictionary that maps the return address (i.e.
  the instruction *after* the call instruction) for each call to the
  avr.CallInfo object.
  """
  text = elf.get_section_by_name('.text')
  data = text.data()
  calls = {}

  for sym in symdict.values():
    offset = sym['st_value']
    end = offset + sym['st_size']
    while offset < end:
      ins = avr.decode_instruction(data, offset, call_only = True)
      call = avr.analyze_call(ins)
      if call:
        ret_addr = ins.addr + ins.info.length
        calls[ret_addr] = call
      offset += ins.info.length
  return calls

def generate_stacktrace(elf, memory, big):
  """
  Generate a stacktrace on stdout from looking at the given memory dump
  and elf file.
  """
  addrlen = 3 if big else 2
  dwarf_info = elf.get_dwarf_info()
  symdict = process_symtab(elf)

  # All call instructions in the program
  callsites = find_callsites(elf, symdict)

  print("Stacktrace follows (most recent call first)")

  # Find all 2 or 3-byte pointers in the stack that match a call
  # instruction (e.g. are likely a return address on the stack)
  addresses = memory.addresses()
  for addr in addresses:
    if all(addr + i in addresses for i in range(addrlen)):
      wordptr = int.from_bytes(memory.tobinstr(start=addr, size=addrlen), byteorder = 'big')
      # Memory contains word addresses, convert to byte addresses
      ptr = wordptr * 2

      if ptr in callsites:
        call = callsites[ptr]
        caller = address_to_containing_function(symdict, call.instruction.addr)
        sys.stdout.write("0x{:06x}: {} in {}".format(call.instruction.addr, call.instruction.info.mnemonic, caller))

        # TODO: This is fairly slow
        location = address_to_location(dwarf_info, call.instruction.addr)
        if location:
          sys.stdout.write(" at {}".format(location))

        if call.callee_addr:
          callee = address_to_function(symdict, call.callee_addr)
          sys.stdout.write(" called {}".format(callee))

        sys.stdout.write("\n")

def main():
  parser = argparse.ArgumentParser(description = 'Analyze AVR memory dumps')
  parser.add_argument('--elf', help='Compiled elf file')
  parser.add_argument('--cppfilt', help='Path to c++filt command')
  parser.add_argument('memory', help='Memory dump file')
  args = parser.parse_args()

  # Store cppfilt option
  global cppfilt
  if args.cppfilt:
    cppfilt = args.cppfilt

  big = False

  # Read elf file if specified
  elf = None
  if args.elf:
    # Note that file is kept open, ELFFile reads from it on the fly.
    elf = ELFFile(open(args.elf, 'rb'))

    if elf['e_machine'] != 'EM_AVR':
      sys.stderr.write("Not an AVR elf file (machine id: 0x%{:04X})\n".format(elf['e_machine']))
      sys.exit(1)

    # https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;a=blob;f=include/elf/avr.h;h=70d750b8c7147501dfc6c9cc2c201028e970171e;hb=HEAD#l27
    # #define EF_AVR_MACH 0x7F
    # #define E_AVR_MACH_AVR6     6
    # #define E_AVR_MACH_AVRTINY 100
    arch = elf['e_flags'] & 0x7F
    if arch >= 100:
      sys.stderr.write("AVR Xmega not supported\n")
      sys.exit(1)

    # avr6 chips have a > 128kbyte flash and need a 3-byte return
    # address
    if arch == 6:
      print("AVR6 architecture detected, assuming 3-byte return addresses")
      big = True

  # Read memory file
  memory = IntelHex(args.memory)

  if elf:
    generate_stacktrace(elf, memory, big)
  else:
    print("Need elf file to generate stack trace")

main()