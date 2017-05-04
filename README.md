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

Running
-------
To run this tool:

    $ ./main.py --isr-return 0x123 --elf program.elf dump.hex

The `isr-return` option can be passed to include the (watchdog) ISR
return address (e.g. where the interrupt occured) in the stacktrace.
This address is printed by the example code, but this option can be
omitted entirely.

Limitations
-----------
When generating the stacktrace:
 - All calls resulting from call instructions (all variants) should be
   present.
 - There might be bogus entries resulting from random data in the stack.
 - Calls to interrupt handlers do not show up, since there is no
   corresponding call instruction.

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
