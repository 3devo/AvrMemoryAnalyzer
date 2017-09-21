/*
Copyright (c) 2014 Matthijs Kooijman <matthijs@stdin.nl> (get_return_address)
Copyright (c) 2017 3devo (www.3devo.eu)

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
*/

#include <util/atomic.h>

inline void init_wdt() {
  wdt_enable(WDTO_4S);
  WDTCSR |= (1 << WDIE);
}

inline void printHex(uint8_t byte) {
  if (byte < 0x10)
    Serial.print('0');
  Serial.print(byte, HEX);
}

inline void printHex(uint16_t byte) {
  if ((uintptr_t)byte < 0x1000)
    Serial.write('0');
  if ((uintptr_t)byte < 0x100)
    Serial.write('0');
  if ((uintptr_t)byte < 0x10)
    Serial.write('0');
  Serial.print((uintptr_t)byte, HEX);
}

inline void dumpLineIhex(uint8_t *addr, uint8_t *end) {
  uint8_t sum = 0;

  Serial.write(':');
  uint8_t len = end - addr;
  // Line length
  printHex(len);
  sum -= len;

  // Addr
  uint16_t intaddr = (uint16_t)addr;
  printHex(intaddr);
  sum -= intaddr >> 8;
  sum -= intaddr & 0xff;

  // Record type
  printHex((uint8_t)0);
  sum -= 0;

  while (addr < end) {
    uint8_t byte = *addr++;
    sum -= byte;
    printHex(byte);
  }
  printHex(sum);
  Serial.println();
}

static const uint8_t LINE_LENGTH = 32;

inline void dumpMemoryIhex(uint8_t *addr, uint8_t *end) {
  while (addr < end) {
    uint8_t *next = addr + LINE_LENGTH;
    if (next > end)
      next = end;
    dumpLineIhex(addr, next);
    addr = next;
  }
  // EOF marker
  Serial.println(F(":00000001FF"));
}

#ifndef __AVR_3_BYTE_PC__
	// On 2-byte PC processors, we can just use the builtin function
	// This returns a word address, not a byte address
	inline uint16_t get_return_address() __attribute__((__always_inline__));
	inline uint16_t get_return_address() { return (uint16_t)__builtin_return_address(0); }
#else
	// On 3-byte PC processors, the builtin doesn't work, so we'll
	// improvise
	// This returns a word address, not a byte address
	inline uint32_t get_return_address() __attribute__((__always_inline__));
	inline uint32_t get_return_address() {
		// Frame layout:
		// [RA0]
		// [RA1]
		// [RA2]
		// ... Variables ...
		// [empty] <-- SP

		// Find out how big the stack usage of the function
		// (into which we are inlined) is. It seems gcc won't
		// tell us, but we can trick the assembler into telling
		// us at runtime.
		uint8_t stack_usage;
		__asm__ __volatile__("ldi %0, .L__stack_usage" : "=r"(stack_usage));

		// Using the stack usage, we can find the top of the
		// frame (the byte below the return address)
		uint8_t *frame_top = (uint8_t*)SP + stack_usage;

		// And then read the return address
		return (uint32_t)frame_top[1] << 16 | (uint16_t)frame_top[2] << 8 | frame_top[3];
	}
#endif

inline void dumpMemory() __attribute__((__always_inline__));
inline void dumpMemory() {
  uint16_t sp;
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    sp = SP;
  }
  Serial.print("SP = 0x");
  Serial.println(sp, HEX);
  Serial.print("Return = 0x");
  Serial.print(get_return_address() * 2, HEX);
  Serial.println(" (byte address)");

  // Dump I/O memory
  dumpMemoryIhex(NULL, (uint8_t*)RAMSTART);
  Serial.println("...");
  // Dump stack (SP is the next unused value, so SP + 1 is the first valid
  // stack value)
  dumpMemoryIhex((uint8_t*)sp + 1, (uint8_t*)RAMEND+1);
}

ISR(WDT_vect) {
  dumpMemory();
}

