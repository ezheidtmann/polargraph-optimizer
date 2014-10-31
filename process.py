#!/usr/bin/python

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
from operator import attrgetter
sorted_g = sorted(glyphs, key=attrgetter('start'))
print("Sorted penup distance:  %9d" % total_penup_travel(sorted_g), file=sys.stderr)
print("Sorted total distance:  %9d" % total_travel(sorted_g), file=sys.stderr)

# Try a few starting points with the greedy sort, just to make sure we don't
# happen to start somewhere crazy.
for i in range(0, len(glyphs), len(glyphs) / 15):
    greedy = reorder_greedy(glyphs, index=i)
    print("Greedy penup (i=%d)      %9d" % (i, total_penup_travel(greedy)), file=sys.stderr)
    print("Greedy total (i=%d)      %9d" % (i, total_travel(greedy)), file=sys.stderr)
    print_glyphs(greedy)
    import sys
    sys.exit()

# Next up: try flipping the ordering of individual glyphs in greedy sort
#
# Other ideas:
#   - Divide drawing into subregions and then optimize each region
#   - Full O(n!) exhaustive search (eek!)
#   - ???
