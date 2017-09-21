AVR memory analyzer
===================
This tool analyzes memory dumps from AVR chips. Currently it assumes
that the entire memory read is the stack and constructs a stacktrace
from it.

Constructing a stacktrace uses a somewhat rough method: It tries to
interpret all data on the stack as if they were return addresses, and
any that would make sense as such (i.e. point the the instruction
following a call instruction) are assumed to actually *be* a return
address and result in an entry in the stacktrace.

This approach should result in a complete stack trace (except for ISRs,
see limitations below), possibly with
some false entries (which were just random data that happened to match a
call instruction).

This approach is based on a tool called `avrstackrev` published by
Atmel (see [the post describing it][post] and [the project page with the
sources][project]). That tool includes some additional machinery for
dumping a stacktrace to EEPROM or dump it through the UART. It also
depends on avr-objdump to disassemble the sources, while this tool reads
the elf file directly.

[post]: http://www.embedded.com/design/debug-and-optimization/4431982/1/How-to-debug-elusive-software-code-problems-without-a-debugger]
[project]: https://spaces.atmel.com/gf/project/avrstackrev

Dumping the stack
-----------------
To do its work, this tool needs a stack dump in Intel hex (.hex) format.
For some example Arduino code that sets up the watchdog timer and makes
a stack dump when the watchdog timer triggers, see `dump_memory.h`.
This code also dumps all I/O registers, for ease of debugging, but these
I/O registers should not be passed to the analyzer (a future version
might analyze these too). The example code contains a `dumpMemory()`
function that can also be separately called at any time to generate a
stack dump.

In addition to dumping memory, the example also prints SP and the return
address of the function calling `dumpMemory()`. The latter can be useful
in an ISR, to show where the interrupt occured (see the `--isr-return`
option for that).

Here's an example of how that could look (IO registers were trimmed for
brevity):

```
SP = 0x21AC
Return = 0x1C62E (byte address)
IO registers:
:20000000000000008C0F0C03B7100200000220004B007300010030210200C0001D00C1009B
:200020000000000DE70101E1010B000BF708000F0F0F202320070F070F0F0F00003C0000BD
:20004000C82C000003034900000000005000B10030000000000000000000000000A1213535
:200060002800000000008D000090050000000100000000000000000000009708470000004F
:00000001FF
Stack:
:202183001BB32197108D1BBE108D0003000D00004E00009E87009E58009E57108D1BB300CA
:2021A3000B44D00082250D6201200083C321C1010D6295AFAE1110A9030C0F7E00D92F329C
:2021C3003031372D303900000000C260218408006E8B4120322E38356D6D000000000000FE
:1D21E30000000040A69B443BCDCCCC3D3030303030300002002F0000268E0026CC46
:00000001FF
Dump complete
```

The "Return" address is the address the ISR will return to, so the point
where the interrupt occured. The IO registers are intended to manually
review for debugging. The stack dump is intended to be processed by this
tool. The dump is in "Intel hex" format, you can create a .hex file by
just copying the lines between "Stack" and "Dump complete" into a plain
text file.

When the stacktrace is long and/or you are using a low baudrate, the
watchdog reset could trigger before the dump is complete. Be sure to
check if the output is complete before trying to analyze it.

Each line (except for the last, shorter line, which serves as an
end-of-file indicator) is built from a one byte line length (usually
0x20 = 32 bytes), a two-byte address, a single-byte record type (0x00
for data lines), the actual data bytes (usually 32) and one checksum
byte.

Running
-------
To run this tool:

    $ ./main.py --isr-return 0x123 --elf program.elf dump.hex

The `isr-return` option can be passed to include the (watchdog) ISR
return address (e.g. where the interrupt occured) in the stacktrace.
This address is printed by the example code, but this option can be
omitted entirely.

For example, to generate a dump from the example output below, the
stack dump is copied into a file `dump.hex`, and we run:

```
./main.py --isr-return 0x13D0E --elf program.elf dump.hex
AVR6 architecture detected, assuming 3-byte return addresses
Stacktrace follows (most recent call first)
0x013d0e: interrupt in StatusComponent::event(Screen*, Event) at Screen.h:1130
0x010448: eicall in Screen::draw_now() at Screen.h:1130
0x010784: eicall in Scheduler::execute() at Screen.h:1130
0x01b25a: call in main at Main.cpp:378 called Scheduler::execute()
```

Note that for indirect calls (`icall` or `eicall`), only the caller is
shown, the called function is not known.

Limitations
-----------
When generating the stacktrace:
 - All calls resulting from call instructions (all variants) should be
   present.
 - There might be bogus entries resulting from random data in the stack.
 - Calls to interrupt handlers do not show up, since there is no
   corresponding call instruction (but the ISR that triggered the dump
   can be shown using `--isr-return`).

For a completely correct stacktrace, this tool should analyze the stack
by figuring out the stack frame sizes of the functions involved, so it
can know where in the stack the return address should be *exactly*.
Doing so needs to either make gcc output stack frame sizes for each
function (which I couldn't figure out how), or analyze the generated
code for each function to figure out the stack frame size (which is
probably hard to get right). I believe gdb does the latter, so
converting a memory dump to a core dump in ELF format that gdb can read
might be a future addition to this tool.

The `dumpMemory()` example code does very limited analysis (only the
most recent frame), which allows analyzing a single ISR frame (if
`dumpMemory()` is called directly from the ISR).

Dependencies
------------
This tool relies on three python libraries:

	pip3 install pyelftools
	pip3 install intelhex
	pip3 install sortedcontainers

In addition, it needs the `c++filt` (or `avr-c++filt`) tool to do
demangling of function names. It assumes the former is available on the
system path, if not pass the full path to the tool using the `--cppfilt`
option. Two python libraries ([1][one], [2][two]) were tested for
demangling, but both seemed to have binary dependencies which didn't
work on a stock Debian system, let alone a Windows system, so an
external tool is used instead.

[one]: https://pypi.python.org/pypi/cxxfilt/0.1.0
[two]: https://github.com/P4N74/demangler

License
-------
Most of the code contained in this repository is licensed under the 3-clause
BSD license, one bit is public domain code. See the individual source files
for the full licensing terms.
