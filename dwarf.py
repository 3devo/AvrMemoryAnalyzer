# This code was originally based on code by Eli Bendersky
# (eliben@gmail.com), which is placed in the public domain. Source:
# https://github.com/eliben/pyelftools/blob/master/examples/dwarf_decode_address.py
# It has since been mostly rewritten.

def get_addr_to_line_map(elf):
  dwarf_info = elf.get_dwarf_info()
  cache = {}

  # Go over all the line programs in the DWARF information, looking for
  # one that describes the given address.
  for CU in dwarf_info.iter_CUs():
    # First, look at line programs to find the file/line for the address
    lineprog = dwarf_info.line_program_for_CU(CU)
    prevstate = None
    ignore_this_sequence = False
    for entry in lineprog.get_entries():
      # DWARF lineinfo is a sequence of instructions, some of
      # which build internal registers, and some which output a
      # new state based on those internal registers. We're only
      # interested in the resulting states, so ignore everything
      # else.
      if entry.state is None:
        continue

      # Each resulting state maps a source line to an address,
      # annotated with some extra info which are not so
      # interesting to us. The only flag which is interesting is
      # the end_sequence flag, which indicates that this address
      # is one-past-the-end of the current sequence of consecutive
      # addresses.

      if not prevstate and entry.state.address == 0:
        # For code that was optimized away at link time, the
        # linker typically emits sequences starting at address 0
        # rather than removing them. Since these addresses make
        # no sense, ignore them.
        ignore_this_sequence = True

      if ignore_this_sequence:
        # Ignore the sequence up to and including the next
        # end_sequence
        if entry.state.end_sequence:
          ignore_this_sequence = False
        continue

      # Record the line number of the previous state for all
      # addresses up to this next state (possibly the
      # end_sequence).
      if prevstate:
        filename = lineprog['file_entry'][prevstate.file - 1].name
        line = prevstate.line
        # Rather than keeping a single entry for the range of
        # addresses fo this line, we add an entry for each
        # address separately. This produces a bigger cache (150k
        # vs 50k entries for a production Arduino STM32 sketch),
        # but also makes querying a lot simpler (and probably
        # faster). There does not seem to be a signficant
        # slowdown in generating the cache (which is dominated
        # by the DWARF info parsing anyway).
        # TODO: Some of these ranges are big (sometimes > 100
        # bytes attributed to a single line). It seems these big
        # ranges are data encoded in the text section, which is
        # common on ARM. These data runs could be detected and
        # skipped using special entries in the symbol table, see
        # https://sourceware.org/bugzilla/show_bug.cgi?id=10263#c1
        # https://developer.arm.com/docs/ihi0044/latest
        for addr in range(prevstate.address, entry.state.address):
          cache[addr] = (filename, line)

      prevstate = entry.state
      if entry.state.end_sequence:
        # This ends the current sequence, so do not use it as
        # prevstate for the next, unrelated, state.
        prevstate = None
  return cache
