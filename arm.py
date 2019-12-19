import sys
from collections import namedtuple

import capstone

def get_arm_tags(elf):
  """ Extract arm-specific tags from the given ELFFile. """
  # Code based on https://github.com/eliben/pyelftools/blob/0ef59f56ff0f1caf09653b412eba5a0c41e368fd/test/test_arm_support.py
  sec = elf.get_section_by_name('.ARM.attributes')
  if not sec or sec['sh_type'] != 'SHT_ARM_ATTRIBUTES' or sec.num_subsections != 1:
    return {}

  subsec = sec.subsections[0]
  if subsec.header['vendor_name'] != 'aeabi' or subsec.num_subsubsections != 1:
    return {}

  subsubsec = subsec.subsubsections[0]
  if subsubsec.header.tag != 'TAG_FILE':
    return {}

  return {attr.tag: attr.value for attr in subsubsec.iter_attributes()}

def reg_str(regnum):
  """ Convert a capstone ARM register number to its name. """
  for name, num in capstone.arm.__dict__.items():
    if name.startswith("ARM_REG_") and num == regnum:
      return name
  return "Unknown reg: {}".format(regnum)

def struct_to_dict(struct):
  """ Convert a ctypes struct to dict for debug printing. """
  return dict((field, getattr(struct, field)) for field, _ in struct._fields_)

def insn_repr(insn):
  """ Provide a debug-printable representation of an instruction. """
  res = [hex(insn.address), insn.mnemonic]
  for op in insn.operands:
    if op.type == capstone.arm.ARM_OP_REG:
      res.append(reg_str(op.reg))
    elif op.type == capstone.arm.ARM_OP_IMM:
      res.append(hex(op.imm))
    elif op.type == capstone.arm.ARM_OP_FP:
      res.append(op.fp)
    elif op.type == capstone.arm.ARM_OP_MEM:
      res.append(struct_to_dict(op.mem))
    else:
      res.append("Unknown op")
  return res

CallInfo = namedtuple('CallInfo', ['mnemonic', 'call_addr', 'callee_addr'])
def analyze_call(insn):
  """ Analyze an instruction and return a CallInfo if it is a call. """

  # Filter any CALL or JUMP instructions. It seems capstone
  # classifies all of these as JUMP (including the
  # branch-and-link which is sortof the call instruction), but
  # still include CALL just in case.
  if not any(g in [capstone.CS_GRP_JUMP, capstone.CS_GRP_CALL] for g in insn.groups):
    return None

  if len(insn.operands) == 1 and insn.operands[0].type == capstone.arm.ARM_OP_IMM:
    # Most branch instructions have just a single immediate operand
    # with the absolute branch address.
    # TODO: This likely also includes all jumps inside functions, too.
    # Maybe limit to entries in the symbol table?
    # TODO: Should this add insn.addr?
    callee_addr = insn.operands[0].imm
  else:
    # Otherwise assume indirect call
    # TODO: This might catch other types of calls too?
    callee_addr = None

  return CallInfo(mnemonic=insn.mnemonic, call_addr=insn.address, callee_addr=callee_addr)

class ArchArm:
  def __init__(self, elf):
    attrs = get_arm_tags(elf)
    cpu_arch = attrs.get('TAG_CPU_ARCH', None)

    if cpu_arch is None:
      raise Exception("No CPU arch tag found, not sure how to proceed")

    # CPU arch values from
    # https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;a=blob;f=include/elf/arm.h;h=75fb5e26ca0b482c7f693d31e66ee78b1254be5b;hb=HEAD#l96
    # and https://static.docs.arm.com/ihi0044/g/aaelf32.pdf (table 5-5)
    if cpu_arch == 13:
      sys.stdout.write("Found ARM7E-M, this is a tested architecture\n")
      # This was tested using a Cortex-M4
    else:
      sys.stdout.write("Warning: CPU arch unknown/untested, disassembly settings might be wrong\n")

    # These are mostly guesses, only tested on ARM7E-M
    # ARM vs THUMB mode is selected per-symbol later
    mode = 0
    if cpu_arch in [11, 12, 13]:
      mode |= capstone.CS_MODE_MCLASS
    if cpu_arch >= 14:
      mode |= capstone.CS_MODE_V8

    if elf.little_endian:
      mode |= capstone.CS_MODE_LITTLE_ENDIAN
    else:
      mode |= capstone.CS_MODE_BIG_ENDIAN

    self.cs = capstone.Cs(capstone.CS_ARCH_ARM, mode)
    self.cs.detail = True

  def get_addrlen(self):
    """ Return the length of a return address on the stack. """
    return 4

  def get_alignment(self):
    """ Return the alignment of a return address on the stack. """
    return 4

  def find_callsites(self, elf, symdict):
    """
    Look through all code in the .text section and identify call
    instructions. Returns a dictionary that maps the return address (i.e.
    the instruction *after* the call instruction) for each call to the
    .CallInfo object.
    """
    text = elf.get_section_by_name('.text')
    data = text.data()
    text_start = text['sh_addr']
    calls = {}

    for sym in symdict.values():
      # The LSB indicates Thumb (1) or ARM (0) instructions.
      if sym['st_value'] & 1 == 0:
        self.cs.mode = self.cs.mode & ~capstone.CS_MODE_THUMB | capstone.CS_MODE_ARM
      else:
        self.cs.mode = self.cs.mode & ~capstone.CS_MODE_ARM | capstone.CS_MODE_THUMB

      sym_addr = sym['st_value'] & ~1
      sym_size = sym['st_size']
      offset = sym_addr - text_start
      end = offset + sym['st_size']
      func = data[offset:end]
      #print("\n%{:08X} <{}>".format(sym_addr, sym.name))

      for insn in self.cs.disasm(func, sym_addr, sym_size):
        call = analyze_call(insn)
        if call:
          ret_addr = insn.address + insn.size
          calls[ret_addr] = call
          #print(insn_repr(insn))

    return calls

  def decode_ptr(self, bytestr):
    """
    Decode a given stack fragment of size addrlen into a return address.
    """

    ptr = int.from_bytes(bytestr, byteorder = 'little')
    # Clear lower bit, which is used to select between ARM/thumb mode
    return ptr & ~0x1

  def sym_to_addr(self, sym):
    """
    Return the address of the given symbol.
    """
    # Clear lower bit, which is used to select between ARM/thumb mode
    return sym['st_value'] & ~0x1

__all__ = ('ArchArm',)
