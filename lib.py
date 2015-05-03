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
            print("Problem with instructions in glyph:", file=sys.stderr)
            for i in instructions:
                print("%s (%s)" % (i.line, i.typename), file=sys.stderr)

        self.instructions = instructions

    def _distance_to_slow(self, other):
        return max(abs(other.start[0] - self.end[0]), abs(other.start[1] - self.end[1]))

    def distance_to(self, other):
        """
        Compute distance between two glyphs (other.start - self.end)

        This is not strictly 'distance', but something which is proportional to
        the time it takes the polargraph to move between positions.  The device
        seems to move each servo independently at the same speed, so the time
        to move betwen points is proportional to the greatest distance each
        servo has to move.
        """
        # Optimized equivalent to:
        #
        #

        zeros = other.start[0] - self.end[0]
        ones = other.start[1] - self.end[1]
        if zeros < 0:
            if ones < 0:
                if zeros < ones:
                    return -zeros
                return -ones
            if -zeros < ones:
                return ones
            return -zeros

        if zeros < ones:
            return ones
        return zeros

    def _distance_to_if_other_reversed_slow(self, other):
        return max(abs(other.end[0] - self.end[0]), abs(other.end[1] - self.end[1]))
    def distance_to_if_other_reversed(self, other):
        zeros = other.end[0] - self.end[0]
        ones = other.end[1] - self.end[1]
        if zeros < 0:
            if ones < 0:
                if zeros < ones:
                    return -zeros
                return -ones
            if -zeros < ones:
                return ones
            return -zeros

        if zeros < ones:
            return ones
        return zeros

    def _reversed_instructions(self):
        """
        A generator of the reversed instructions.

        Typical instructions look like this (normal ordering):

        C17,2638,6563,2,END <-- startpoint (assumed pen is up)
        C13,END             <-- pendown
        C17,2679,6558,2,END <-- drawing moves ...
        C17,2677,6569,2,END
        C17,2663,6573,2,END <-- last move
        C14,END             <-- penup

        So a reversed ordering would print in this order:

        last move
        pendown
        other moves in reversed order
        startpoint
        penup

        """
        original_order = iter(self.instructions)
        reverse_order = reversed(self.instructions)

        startpoint = next(original_order)
        pendown = next(original_order)

        penup = next(reverse_order)
        endpoint = next(reverse_order)

        yield endpoint
        yield pendown

        for i in reverse_order:
            if not i.typename == 'move':
                break
            yield i

        yield startpoint
        yield penup

    def ordered_instructions(self):
        if self._reversed:
            return self._reversed_instructions()
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
    from operator import itemgetter
    gs = list(gs)
    ordered = [gs.pop(index)]
    prev = ordered[0]

    def dist_reverse_iterator(gs):
        for g in gs:
            yield (prev.distance_to(g), False, g)
            yield (prev.distance_to_if_other_reversed(g), True, g)

    while len(gs) > 0:
        (dist, reverse, nearest) = min(dist_reverse_iterator(gs),
                                       key=itemgetter(0, 1))
        gs.remove(nearest)

        if reverse:
            prev = nearest.reversed_copy()
        else:
            prev = nearest

        ordered.append(prev)

    return ordered

def prune_zero_distance_penups(instructions):
    instructions = iter(instructions)
    try:
        prev = next(instructions)
    except StopIteration:
        raise ValueError("instructions empty")
    # The first instruction should always be a penup, so we send it straight
    # through.
    yield prev

    try:
        while True:
            current = next(instructions)
            if current.typename == 'penup':
                last_down = prev
                penup = current

                # Get all moves while the pen is up. There should only ever be
                # one, but you never know these days. :-)
                moves = []
                try:
                    while True:
                        penup_move = next(instructions)
                        if penup_move.typename == 'pendown':
                            pendown = penup_move
                            break
                        else:
                            moves.append(penup_move)
                except StopIteration:
                    # If we reach the end of the instructions while looking for
                    # a pendown, raise the pen and call it good.
                    yield penup
                    raise StopIteration

                if moves[-1].coords == last_down.coords:
                    # The penup move(s) didn't go anywhere, so we remove them
                    # from the list of instructions and continue to the next
                    # instruction.
                    continue
                else:
                    # The penup move(s) DID actually move, so we keep them.
                    yield penup
                    for move in moves:
                        yield move
                    yield pendown
            else:
                yield current
            prev = current

    except StopIteration:
        pass


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

def iter_instructions(gs):
    # be sure to start with a penup
    yield Instruction('C14,END')
    for g in gs:
        for i in g.ordered_instructions():
            yield i
