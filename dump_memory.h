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

#if defined(__AVR__)
#include <util/atomic.h>
#include <avr/wdt.h>
#endif


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

inline void printHex(uint32_t byte) {
  if ((uintptr_t)byte < 0x10000000)
    Serial.write('0');
  if ((uintptr_t)byte < 0x1000000)
    Serial.write('0');
  if ((uintptr_t)byte < 0x100000)
    Serial.write('0');
  if ((uintptr_t)byte < 0x10000)
    Serial.write('0');
  if ((uintptr_t)byte < 0x1000)
    Serial.write('0');
  if ((uintptr_t)byte < 0x100)
    Serial.write('0');
  if ((uintptr_t)byte < 0x10)
    Serial.write('0');
  Serial.print((uintptr_t)byte, HEX);
}

inline void dumpExtAddrLineIhex(uint16_t upper_addr) {
  // Since normal records only have 16 address bit, this special record
  // sets the upper 16 address bits to be a prepended to all subsequent
  // records.
  Serial.print(":02000004");
  printHex(upper_addr);

  uint8_t sum = 0 - 2 - 4 - (upper_addr >> 8) - (upper_addr & 0xff);
  printHex(sum);
  Serial.println();
}

inline void dumpLineIhex(uint8_t *addr, uint8_t *end, uint8_t *prev_addr) {
  uint8_t sum = 0;

  uintptr_t intaddr = (uintptr_t)addr;
  if ((intaddr >> 16) != ((uintptr_t)prev_addr >> 16))
    dumpExtAddrLineIhex(intaddr >> 16);

  Serial.write(':');
  uint8_t len = end - addr;
  // Line length
  printHex(len);
  sum -= len;

  // Addr
  uint16_t addr16 = (uint16_t)intaddr;
  printHex(addr16);
  sum -= addr16 >> 8;
  sum -= addr16 & 0xff;

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
  uint8_t *prev_addr = nullptr;
  while (addr < end) {
    uint8_t *next = addr + LINE_LENGTH;
    if (next > end)
      next = end;
    dumpLineIhex(addr, next, prev_addr);
    prev_addr = addr;
    addr = next;
  }
  // EOF marker
  Serial.println(F(":00000001FF"));
}

#ifndef __AVR_3_BYTE_PC__
  // On 2-byte PC processors (or non-AVR), we can just use the builtin function
  // On AVR, this returns a word address, not a byte address
  inline uintptr_t get_return_address() __attribute__((__always_inline__));
  inline uintptr_t get_return_address() { return (uintptr_t)__builtin_return_address(0); }

  using retaddr_t = uintptr_t;
#else
  // On AVR 3-byte PC processors, the builtin doesn't work, so we'll
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

  // We also need a retaddr variable that is bigger than uintptr_t
  using retaddr_t = uint32_t;
#endif

inline void dumpMemory() __attribute__((__always_inline__));
#if defined(__AVR__)
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
  Serial.println("IO registers:");
  dumpMemoryIhex(NULL, (uint8_t*)RAMSTART);
  Serial.println("Stack:");
  // Dump stack (SP is the next unused value, so SP + 1 is the first valid
  // stack value)
  dumpMemoryIhex((uint8_t*)sp + 1, (uint8_t*)RAMEND+1);
  Serial.println("Dump complete");
  // Ensure the output is transmitted before returning from the ISR
  Serial.flush();
}

inline void init_wdt() {
  // Note that this enables the watchdog interrupt, but also keeps the
  // watchdog itself enabled. The first time the watchdog triggers, the
  // interrupt runs and dumps the stack, but the second time it
  // triggers, the system is reset to prevent deadlock. This could cause
  // the memory output to be cut short (especially on low baudrates).
  wdt_enable(WDTO_4S);
  WDTCSR |= (1 << WDIE);
}

ISR(WDT_vect) {
  dumpMemory();
}

#elif defined(ARDUINO_ARCH_STM32)
void dumpMemory() {
  sp = __get_MSP();
  Serial.print("SP = 0x");
  Serial.println(sp, HEX);
  Serial.print("Return = 0x");
  Serial.print(get_return_address(), HEX);
  Serial.println(" (byte address)");

  // I/O memory is fragmented over different devices on STM32, so do not
  // dump that here.

  Serial.println("Stack:");
  // Dump stack (SP is the first used value)
  dumpMemoryIhex((uint8_t*)sp, (uint8_t*)&_estack);
  // Ensure the output is transmitted before returning from the ISR
  Serial.flush();
}
#endif
