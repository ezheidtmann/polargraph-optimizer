#!/usr/bin/python

from __future__ import print_function
from lib import *

######################

instructions = []

import fileinput
for line in fileinput.input():
    instructions.append(Instruction(line))

glyphs = []
chunk = []
for inst in instructions:
    chunk.append(inst)
    if inst.typename == 'penup':
        if len(chunk) > 1:
            glyphs.append(Glyph(chunk))
        chunk = []

print("Total Glyphs: %d" % len(glyphs), file=sys.stderr)

# No sorting
print("Initial penup distance: %9d" % total_penup_travel(glyphs), file=sys.stderr)
print("Initial total distance: %9d" % total_travel(glyphs), file=sys.stderr)

# dedupe alone (and used below)
glyphs = list(dedupe(glyphs))
print("Deduped penup distance: %9d" % total_penup_travel(glyphs), file=sys.stderr)
print("Deduped total distance: %9d" % total_travel(glyphs), file=sys.stderr)

# easy sort: sort all glyphs by starting point
#
# This is O(n log n) because it's simply a sort.
sorted_g = sorted(glyphs,
                  key=lambda st: st.start or tuple())  # add default key in case 'start' is missing.
print("Sorted penup distance:  %9d" % total_penup_travel(sorted_g), file=sys.stderr)
print("Sorted total distance:  %9d" % total_travel(sorted_g), file=sys.stderr)

i = 0
greedy = reorder_greedy(glyphs, index=i)
print("Greedy penup (i=%1d)      %9d" % (i, total_penup_travel(greedy)), file=sys.stderr)
print("Greedy total (i=%1d)      %9d" % (i, total_travel(greedy)), file=sys.stderr)

# Render down from Glyphs -> Instructions
instructions = list(iter_instructions(greedy))
print("Total instructions:     %9d" % (len(instructions),), file=sys.stderr)
# Remove penup / move / pendown sequences that don't actually move anywhere.
pruned_instructions = list(prune_zero_distance_penups(instructions))
print("Pruned instructions:    %9d" % (len(pruned_instructions),), file=sys.stderr)

for i in pruned_instructions:
    print(i.line)

# Next up: try flipping the ordering of individual glyphs in greedy sort
#
# Other ideas:
#   - Divide drawing into subregions and then optimize each region
#   - Full O(n!) exhaustive search (eek!)
#   - ???
