#!/usr/bin/python

from __future__ import print_function
import sys

class Instruction():
    types = {
        'C13': 'pendown',
        'C14': 'penup',
        'C17': 'move',
    }

    def __init__(self, line):
        self.line = line.rstrip()
        self.parts = self.line.split(',')
        self.typecode = self.parts[0]
        self.typename = self._typename()

        self.coords = self._coords()

    def distance_to(self, other):
        return max(abs(other.coords[0] - self.coords[0]), abs(other.coords[1] - self.coords[1]))

    def _typename(self):
        return self.types.get(self.typecode, 'other')

    def _coords(self):
        try:
            return (int(self.parts[1]), int(self.parts[2]))
        except ValueError:
            return None

class Glyph():
    def __init__(self, instructions):
        self._reversed = False
        try:
            self.start = instructions[0].coords
            self.end = instructions[-2].coords
        except IndexError:
            self.start = None
            self.end = None

        if self.start == None or self.end == None:
            print("Problem with instruction set", file=sys.stderr)
            for i in instructions:
                print("%s (%s)" % (i.line, i.typename), file=sys.stderr)

        self.instructions = instructions

    def distance_to(self, other):
        """
        Compute distance between two glyphs (other.start - self.end)

        This is not strictly 'distance', but something which is proportional to
        the time it takes the polargraph to move between positions.  The device
        seems to move each servo independently at the same speed, so the time
        to move betwen points is proportional to the greatest distance each
        servo has to move.
        """
        return max(abs(other.start[0] - self.end[0]), abs(other.start[1] - self.end[1]))

    def distance_to_if_self_reversed(self, other):
        return max(abs(other.start[0] - self.start[0]), abs(other.start[1] - self.start[1]))

    def distance_to_if_other_reversed(self, other):
        #dist_else = self.distance_to(other)
        dist_if = max(abs(other.end[0] - self.end[0]), abs(other.end[1] - self.end[1]))
        return dist_if
        if dist_else == dist_if:
            print("normal: %9d reversed: %9d" % (dist_else, dist_if), file=sys.stderr)
            print("self", file=sys.stderr)
            print("  %5d, %5d start" % self.start,  file=sys.stderr)
            print("  %5d, %5d end"   % self.end,    file=sys.stderr)
            print("other", file=sys.stderr)
            print("  %5d, %5d start" % other.start, file=sys.stderr)
            print("  %5d, %5d end"   % other.end,   file=sys.stderr)

    def ordered_instructions(self):
        if self._reversed:
            print("REVERSED", file=sys.stderr)
            return reversed(self.instructions)
        else:
            return iter(self.instructions)

    def reversed_copy(self):
        if not hasattr(self, '_reversed_copy'):
            from copy import copy
            new = copy(self)
            new.start = self.end
            new.end = self.start
            new._reversed = True
            new._reversed_copy = self
            self._reversed_copy = new
        return self._reversed_copy

    def __hash__(self):
        return hash("\n".join([i.line for i in self.instructions]))

def total_penup_travel(gs):
    """
    Compute total distance traveled in a given ordering
    """
    def distance_between_each_pair(gs):
        gs = iter(gs)
        prev = next(gs)
        for g in gs:
            yield prev.distance_to(g)
            prev = g

    return sum(distance_between_each_pair(gs))

def total_travel(gs):
    def iter_moves(gs):
        for g in gs:
            for i in g.ordered_instructions():
                if i.typename == 'move':
                    yield i

    def distance_between_moves(moves):
        moves = iter(moves)
        prev = next(moves)
        for m in moves:
            yield prev.distance_to(m)
            prev = m

    return sum(distance_between_moves(iter_moves(gs)))

def reorder_greedy(gs, index=0):
    """
    Greedy sorting: pick a starting glyph, then find the glyph which starts
    nearest to the previous ending point.

    This is O(n^2). Pretty sure it can't be optimized into a sort.
    """
    gs = list(gs)
    ordered = [gs.pop(index)]
    prev = ordered[0]
    while len(gs) > 0:
        from operator import methodcaller
        def dist_with_reverse_flag(g):
            return min([
                (prev.distance_to(g), 0, False, g),
                (prev.distance_to_if_other_reversed(g), 1, True, g)
            ])

        (dist, tiebreaker, reverse, nearest) = min(map(dist_with_reverse_flag, gs))
        gs.remove(nearest)

        if reverse:
            prev = nearest.reversed_copy()
        else:
            prev = nearest

        ordered.append(prev)

    return ordered

def dedupe(gs):
    "Use Glyph.__hash__() to dedupe the list of glyphs"
    seen = set()
    for g in gs:
        h = hash(g)
        if h not in seen:
            yield g
            seen.add(h)

def print_glyphs(gs):
    # be sure to start with a penup
    print("C14,END")
    for g in gs:
        for i in g.ordered_instructions():
            print(i.line)

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
