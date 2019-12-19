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

from collections import namedtuple

InstructionInfo = namedtuple('InstructionInfo', ['mnemonic', 'length', 'opcode', 'operands'])
OperandInfo = namedtuple('OperandInfo', ['kind', 'mask'])

# This table was based on revision e9afea4 of
# https://github.com/vsergeev/vavrdisasm/blob/master/avr/avr_instruction_set.c
instructions = [
  InstructionInfo("break", length = 2, opcode = 0x9598, operands = []),
  InstructionInfo("clc", length = 2, opcode = 0x9488, operands = []),
  InstructionInfo("clh", length = 2, opcode = 0x94d8, operands = []),
  InstructionInfo("cli", length = 2, opcode = 0x94f8, operands = []),
  InstructionInfo("cln", length = 2, opcode = 0x94a8, operands = []),
  InstructionInfo("cls", length = 2, opcode = 0x94c8, operands = []),
  InstructionInfo("clt", length = 2, opcode = 0x94e8, operands = []),
  InstructionInfo("clv", length = 2, opcode = 0x94b8, operands = []),
  InstructionInfo("clz", length = 2, opcode = 0x9498, operands = []),
  InstructionInfo("eicall", length = 2, opcode = 0x9519, operands = []),
  InstructionInfo("eijmp", length = 2, opcode = 0x9419, operands = []),
  InstructionInfo("elpm", length = 2, opcode = 0x95d8, operands = []),
  InstructionInfo("icall", length = 2, opcode = 0x9509, operands = []),
  InstructionInfo("ijmp", length = 2, opcode = 0x9409, operands = []),
  InstructionInfo("lpm", length = 2, opcode = 0x95c8, operands = []),
  InstructionInfo("nop", length = 2, opcode = 0x0000, operands = []),
  InstructionInfo("ret", length = 2, opcode = 0x9508, operands = []),
  InstructionInfo("reti", length = 2, opcode = 0x9518, operands = []),
  InstructionInfo("sec", length = 2, opcode = 0x9408, operands = []),
  InstructionInfo("seh", length = 2, opcode = 0x9458, operands = []),
  InstructionInfo("sei", length = 2, opcode = 0x9478, operands = []),
  InstructionInfo("sen", length = 2, opcode = 0x9428, operands = []),
  InstructionInfo("ses", length = 2, opcode = 0x9448, operands = []),
  InstructionInfo("set", length = 2, opcode = 0x9468, operands = []),
  InstructionInfo("sev", length = 2, opcode = 0x9438, operands = []),
  InstructionInfo("sez", length = 2, opcode = 0x9418, operands = []),
  InstructionInfo("sleep", length = 2, opcode = 0x9588, operands = []),
  InstructionInfo("spm", length = 2, opcode = 0x95e8, operands = []),
  InstructionInfo("spm", length = 2, opcode = 0x95f8, operands = [OperandInfo(kind='OPERAND_ZP', mask=0x0000), ]),
  InstructionInfo("wdr", length = 2, opcode = 0x95a8, operands = []),
  InstructionInfo("des", length = 2, opcode = 0x940b, operands = [OperandInfo(kind='OPERAND_DES_ROUND', mask=0x00f0), ]),
  InstructionInfo("asr", length = 2, opcode = 0x9405, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("bclr", length = 2, opcode = 0x9488, operands = [OperandInfo(kind='OPERAND_BIT', mask=0x0070), ]),
  InstructionInfo("brcc", length = 2, opcode = 0xf400, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brcs", length = 2, opcode = 0xf000, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("breq", length = 2, opcode = 0xf001, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brge", length = 2, opcode = 0xf404, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brhc", length = 2, opcode = 0xf405, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brhs", length = 2, opcode = 0xf005, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brid", length = 2, opcode = 0xf407, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brie", length = 2, opcode = 0xf007, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brlo", length = 2, opcode = 0xf000, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brlt", length = 2, opcode = 0xf004, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brmi", length = 2, opcode = 0xf002, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brne", length = 2, opcode = 0xf401, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brpl", length = 2, opcode = 0xf402, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brsh", length = 2, opcode = 0xf400, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brtc", length = 2, opcode = 0xf406, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brts", length = 2, opcode = 0xf006, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brvc", length = 2, opcode = 0xf403, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("brvs", length = 2, opcode = 0xf003, operands = [OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8), ]),
  InstructionInfo("bset", length = 2, opcode = 0x9408, operands = [OperandInfo(kind='OPERAND_BIT', mask=0x0070), ]),
  InstructionInfo("call", length = 4, opcode = 0x940e, operands = [OperandInfo(kind='OPERAND_LONG_ABSOLUTE_ADDRESS', mask=0x01f1), ]),
  InstructionInfo("com", length = 2, opcode = 0x9400, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("dec", length = 2, opcode = 0x940a, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("inc", length = 2, opcode = 0x9403, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("jmp", length = 4, opcode = 0x940c, operands = [OperandInfo(kind='OPERAND_LONG_ABSOLUTE_ADDRESS', mask=0x01f1), ]),
  InstructionInfo("lpm", length = 2, opcode = 0x9004, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_Z', mask=0x0000)]),
  InstructionInfo("lpm", length = 2, opcode = 0x9005, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_ZP', mask=0x0000)]),
  InstructionInfo("lsr", length = 2, opcode = 0x9406, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("neg", length = 2, opcode = 0x9401, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("pop", length = 2, opcode = 0x900f, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("xch", length = 2, opcode = 0x9204, operands = [OperandInfo(kind='OPERAND_Z', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("las", length = 2, opcode = 0x9205, operands = [OperandInfo(kind='OPERAND_Z', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("lac", length = 2, opcode = 0x9206, operands = [OperandInfo(kind='OPERAND_Z', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("lat", length = 2, opcode = 0x9207, operands = [OperandInfo(kind='OPERAND_Z', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("push", length = 2, opcode = 0x920f, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("rcall", length = 2, opcode = 0xd000, operands = [OperandInfo(kind='OPERAND_RELATIVE_ADDRESS', mask=0x0fff), ]),
  InstructionInfo("rjmp", length = 2, opcode = 0xc000, operands = [OperandInfo(kind='OPERAND_RELATIVE_ADDRESS', mask=0x0fff), ]),
  InstructionInfo("ror", length = 2, opcode = 0x9407, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("ser", length = 2, opcode = 0xef0f, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), ]),
  InstructionInfo("swap", length = 2, opcode = 0x9402, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), ]),
  InstructionInfo("adc", length = 2, opcode = 0x1c00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("add", length = 2, opcode = 0x0c00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("adiw", length = 2, opcode = 0x9600, operands = [OperandInfo(kind='OPERAND_REGISTER_EVEN_PAIR_STARTR24', mask=0x0030), OperandInfo(kind='OPERAND_DATA', mask=0x00cf)]),
  InstructionInfo("and", length = 2, opcode = 0x2000, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("andi", length = 2, opcode = 0x7000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
  InstructionInfo("bld", length = 2, opcode = 0xf800, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("brbc", length = 2, opcode = 0xf400, operands = [OperandInfo(kind='OPERAND_BIT', mask=0x0007), OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8)]),
  InstructionInfo("brbs", length = 2, opcode = 0xf000, operands = [OperandInfo(kind='OPERAND_BIT', mask=0x0007), OperandInfo(kind='OPERAND_BRANCH_ADDRESS', mask=0x03f8)]),
  InstructionInfo("bst", length = 2, opcode = 0xfa00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("cbi", length = 2, opcode = 0x9800, operands = [OperandInfo(kind='OPERAND_IO_REGISTER', mask=0x00f8), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("cp", length = 2, opcode = 0x1400, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("cpc", length = 2, opcode = 0x0400, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("cpi", length = 2, opcode = 0x3000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
  InstructionInfo("cpse", length = 2, opcode = 0x1000, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("elpm", length = 2, opcode = 0x9006, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_Z', mask=0x0000)]),
  InstructionInfo("elpm", length = 2, opcode = 0x9007, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_ZP', mask=0x0000)]),
  InstructionInfo("eor", length = 2, opcode = 0x2400, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("fmul", length = 2, opcode = 0x0308, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0070), OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0007)]),
  InstructionInfo("fmuls", length = 2, opcode = 0x0380, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0070), OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0007)]),
  InstructionInfo("fmulsu", length = 2, opcode = 0x0388, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0070), OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0007)]),
  InstructionInfo("in", length = 2, opcode = 0xb000, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_DATA', mask=0x060f)]),
  InstructionInfo("ld", length = 2, opcode = 0x900c, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_X', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x900d, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_XP', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x900e, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_MX', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x8008, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_Y', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x9009, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_YP', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x900a, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_MY', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x8000, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_Z', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x9001, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_ZP', mask=0x0000)]),
  InstructionInfo("ld", length = 2, opcode = 0x9002, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_MZ', mask=0x0000)]),
  InstructionInfo("ldd", length = 2, opcode = 0x8008, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_YPQ', mask=0x2c07)]),
  InstructionInfo("ldd", length = 2, opcode = 0x8000, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_ZPQ', mask=0x2c07)]),
  InstructionInfo("ldi", length = 2, opcode = 0xe000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
  InstructionInfo("lds", length = 4, opcode = 0x9000, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_LONG_ABSOLUTE_ADDRESS', mask=0x0000)]),
  InstructionInfo("lds", length = 2, opcode = 0xA000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x070f)]),
  InstructionInfo("mov", length = 2, opcode = 0x2c00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("movw", length = 2, opcode = 0x0100, operands = [OperandInfo(kind='OPERAND_REGISTER_EVEN_PAIR', mask=0x00f0), OperandInfo(kind='OPERAND_REGISTER_EVEN_PAIR', mask=0x000f)]),
  InstructionInfo("mul", length = 2, opcode = 0x9c00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("muls", length = 2, opcode = 0x0200, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x000f)]),
  InstructionInfo("mulsu", length = 2, opcode = 0x0300, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0070), OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x0007)]),
  InstructionInfo("or", length = 2, opcode = 0x2800, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("ori", length = 2, opcode = 0x6000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
  InstructionInfo("out", length = 2, opcode = 0xb800, operands = [OperandInfo(kind='OPERAND_IO_REGISTER', mask=0x060f), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("sbc", length = 2, opcode = 0x0800, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("sbci", length = 2, opcode = 0x4000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
  InstructionInfo("sbi", length = 2, opcode = 0x9a00, operands = [OperandInfo(kind='OPERAND_IO_REGISTER', mask=0x00f8), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("sbic", length = 2, opcode = 0x9900, operands = [OperandInfo(kind='OPERAND_IO_REGISTER', mask=0x00f8), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("sbis", length = 2, opcode = 0x9b00, operands = [OperandInfo(kind='OPERAND_IO_REGISTER', mask=0x00f8), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("sbiw", length = 2, opcode = 0x9700, operands = [OperandInfo(kind='OPERAND_REGISTER_EVEN_PAIR_STARTR24', mask=0x0030), OperandInfo(kind='OPERAND_DATA', mask=0x00cf)]),
  InstructionInfo("sbr", length = 2, opcode = 0x6000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
  InstructionInfo("sbrc", length = 2, opcode = 0xfc00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("sbrs", length = 2, opcode = 0xfe00, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_BIT', mask=0x0007)]),
  InstructionInfo("st", length = 2, opcode = 0x920c, operands = [OperandInfo(kind='OPERAND_X', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x920d, operands = [OperandInfo(kind='OPERAND_XP', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x920e, operands = [OperandInfo(kind='OPERAND_MX', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x8208, operands = [OperandInfo(kind='OPERAND_Y', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x9209, operands = [OperandInfo(kind='OPERAND_YP', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x920a, operands = [OperandInfo(kind='OPERAND_MY', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x8200, operands = [OperandInfo(kind='OPERAND_Z', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x9201, operands = [OperandInfo(kind='OPERAND_ZP', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("st", length = 2, opcode = 0x9202, operands = [OperandInfo(kind='OPERAND_MZ', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("std", length = 2, opcode = 0x8208, operands = [OperandInfo(kind='OPERAND_YPQ', mask=0x2c07), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("std", length = 2, opcode = 0x8200, operands = [OperandInfo(kind='OPERAND_ZPQ', mask=0x2c07), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("sts", length = 4, opcode = 0x9200, operands = [OperandInfo(kind='OPERAND_LONG_ABSOLUTE_ADDRESS', mask=0x0000), OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0)]),
  InstructionInfo("sts", length = 2, opcode = 0xA800, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x070f)]),
  InstructionInfo("sub", length = 2, opcode = 0x1800, operands = [OperandInfo(kind='OPERAND_REGISTER', mask=0x01f0), OperandInfo(kind='OPERAND_REGISTER', mask=0x020f)]),
  InstructionInfo("subi", length = 2, opcode = 0x5000, operands = [OperandInfo(kind='OPERAND_REGISTER_STARTR16', mask=0x00f0), OperandInfo(kind='OPERAND_DATA', mask=0x0f0f)]),
]

# Reduced set of instructions, containing only call instructions and
# long instructions, to speed up decoding when only call instructions
# are relevant
call_and_long_instructions = [
  ins for ins in instructions
  if 'call' in ins.mnemonic or ins.length > 2
]

unknown_instruction = InstructionInfo("<unknown>", length = 2, opcode = 0x0, operands = [])

def decode_operand(words, info, operand):
  # TODO: Handle non-consecutive bits
  res = words[0] & operand.mask
  if operand.kind == 'OPERAND_LONG_ABSOLUTE_ADDRESS':
    res = res << 16 | words[1]
  return res

Instruction = namedtuple('Instruction', ['addr', 'info', 'raw', 'operands'])

# TODO: Precalculate instruction lookup table for faster decoding
def decode_instruction(data, offset, call_only = False):
  # The upper (and often only) 2-byte word in the instruction identifies
  # the instruction. Note that each word is little-endian internally,
  # but the words themselves are big endian...
  opcode = int.from_bytes(data[offset:offset+2], byteorder='little')
  candidates = instructions
  if call_only:
    candidates = call_and_long_instructions

  for info in candidates:
    # Clear out all operands from the opcode
    masked = opcode
    for operand in info.operands:
      masked &= ~operand.mask
    # See if it now matches the opcode from the table
    if masked == info.opcode:
      # Read the instructions (2 or 4 bytes), shown as big-endian
      raw = hex(int.from_bytes(data[offset:offset+info.length], byteorder='big'))
      words = [int.from_bytes(data[offset+i*2:offset+i*2+2], byteorder='little') for i in range(info.length//2)]
      # Figure out operand values
      operands = []
      for operand in info.operands:
        operands.append(decode_operand(words, info, operand))
      return Instruction(offset, info, raw, operands)

  return Instruction(addr=offset, info=unknown_instruction, raw=0, operands=[])

CallInfo = namedtuple('CallInfo', ['mnemonic', 'call_addr', 'callee_addr'])
def analyze_call(ins):
  """ Analyze an instruction and return a CallInfo if it is a call. """
  if ins.info.mnemonic == 'call':
    callee_addr = ins.operands[0] * 2
  elif ins.info.mnemonic == 'rcall' and ins.operands[0] == 0:
    # gcc uses rcall 0 instructions as a way to advance SP by 2/3 bytes
    # when setting up the stack frame. This is never a meaningful call,
    # so just ignore them.
    return None
  elif ins.info.mnemonic == 'rcall':
    callee_addr = ins.addr + (ins.operands[0] + 1) * 2
  elif ins.info.mnemonic == 'icall' or ins.info.mnemonic == 'eicall':
    callee_addr = None
  else:
    return None

  return CallInfo(mnemonic=ins.info.mnemonic, call_addr=ins.addr, callee_addr=callee_addr)

class ArchAvr:
  def __init__(self, elf):
      # https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;a=blob;f=include/elf/avr.h;h=70d750b8c7147501dfc6c9cc2c201028e970171e;hb=HEAD#l27
      # #define EF_AVR_MACH 0x7F
      # #define E_AVR_MACH_AVR6     6
      # #define E_AVR_MACH_AVRTINY 100
      arch = elf['e_flags'] & 0x7F
      if arch >= 100:
        raise Exception("AVR Xmega not supported\n")
        sys.exit(1)

      # avr6 chips have a > 128kbyte flash and need a 3-byte return
      # address
      if arch == 6:
        print("AVR6 architecture detected, assuming 3-byte return addresses")
        self.addrlen = 3
      self.addrlen = 2

  def get_addrlen(self):
    """ Return the length of a return address on the stack. """
    return self.addrlen

  def get_alignment(self):
    """ Return the alignment of a return address on the stack. """
    return 1

  def find_callsites(self, elf, symdict):
    """
    Look through all code in the .text section and identify call
    instructions. Returns a dictionary that maps the return address (i.e.
    the instruction *after* the call instruction) for each call to the
    CallInfo object.
    """
    text = elf.get_section_by_name('.text')
    data = text.data()
    calls = {}

    for sym in symdict.values():
      offset = sym['st_value']
      end = offset + sym['st_size']
      while offset < end:
        ins = decode_instruction(data, offset, call_only = True)
        call = analyze_call(ins)
        if call:
          ret_addr = ins.addr + ins.info.length
          calls[ret_addr] = call
        offset += ins.info.length
    return calls

  def decode_ptr(self, bytestr):
    """
    Decode a given stack fragment of size addrlen into a return address.
    """

    wordptr = int.from_bytes(bytestr, byteorder = 'big')

    # Memory contains word addresses, convert to byte addresses
    return wordptr * 2

  def sym_to_addr(self, sym):
    """
    Return the address of the given symbol.
    """
    return sym['st_value']

__all__ = ('ArchAvr',)
