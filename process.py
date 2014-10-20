#!/usr/bin/python


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
        try:
            self.start = instructions[0].coords
            self.end = instructions[-2].coords
        except IndexError:
            self.start = None
            self.end = None

        if self.start == None or self.end == None:
            print "Problem with instruction set"
            for i in instructions:
                print "%s (%s)" % (i.line, i.typename)

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
            for i in g.instructions:
                if i.typename == 'move':
                    yield i

    def distance_between_moves(moves):
        moves = iter(moves)
        prev = next(moves)
        for m in moves:
            yield m.distance_to(prev)
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
        nearest = min(gs, key=methodcaller('distance_to', prev))
        gs.remove(nearest)
        ordered.append(nearest)
        prev = nearest
        #if len(gs) % 200 == 0:
        #    print "len: %d" % len(gs)

    return ordered

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

#for glyph in glyphs:
#    print "GLYPH start: %s" % glyph.start
#    print "GLYPH end:   %s" % glyph.end

print "Total Glyphs: %d" % len(glyphs)

# No sorting
print "Initial penup distance: %d" % total_penup_travel(glyphs)
print "Initial total distance: %d" % total_travel(glyphs)

# easy sort: sort all glyphs by starting point
#
# This is O(n log n) because it's simply a sort.
from operator import attrgetter
sorted_g = sorted(glyphs, key=attrgetter('start'))
print "Sorted penup distance:  %d" % total_penup_travel(sorted_g)
print "Sorted total distance: %d" % total_travel(sorted_g)

# Try a few starting points with the greedy sort, just to make sure we don't
# happen to start somewhere crazy.
for i in range(0, len(glyphs), len(glyphs) / 15):
    greedy = reorder_greedy(glyphs, index=i)
    print "Greedy penup (i=%d) %d" % (i, total_penup_travel(greedy))
    print "Greedy total (i=%d) %d" % (i, total_travel(greedy))

# Next up: try flipping the ordering of individual glyphs in greedy sort
#
# Other ideas:
#   - Divide drawing into subregions and then optimize each region
#   - Full O(n!) exhaustive search (eek!)
#   - ???
