#!/usr/bin/python

from __future__ import print_function
from lib import *
import unittest

from itertools import tee
try:
    from itertools import izip
except ImportError:
    izip = zip

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class TestLib(unittest.TestCase):
    def makeGlyphFromText(self, lines):
        instructions = []
        for line in lines.split("\n"):
            line = line.strip()
            if len(line):
                instructions.append(Instruction(line))

        return Glyph(instructions)

    def setUp(self):
        lines = """
        C17,2541,6525,2,END
        C13,END
        C17,2545,6523,2,END
        C17,2664,6506,2,END
        C17,2668,6508,2,END
        C17,2670,6512,2,END
        C17,2663,6534,2,END
        C17,2667,6534,2,END
        C17,2666,6540,2,END
        C17,2645,6543,2,END
        C17,2645,6537,2,END
        C17,2643,6531,2,END
        C17,2633,6527,2,END
        C17,2573,6535,2,END
        C17,2573,6538,2,END
        C14,END
        """

        self.glyph = self.makeGlyphFromText(lines)

    def test_reversing(self):
        text = "\n".join([i.line for i in self.glyph._reversed_instructions()])
        expected_text = """
        C17,2573,6538,2,END
        C13,END
        C17,2573,6535,2,END
        C17,2633,6527,2,END
        C17,2643,6531,2,END
        C17,2645,6537,2,END
        C17,2645,6543,2,END
        C17,2666,6540,2,END
        C17,2667,6534,2,END
        C17,2663,6534,2,END
        C17,2670,6512,2,END
        C17,2668,6508,2,END
        C17,2664,6506,2,END
        C17,2545,6523,2,END
        C17,2541,6525,2,END
        C14,END
        """
        expected_text = "\n".join([l.strip() for l in expected_text.strip().split("\n")])

        self.assertEqual(expected_text, text)

    def test_greedy_sorting(self):
        """
        Exercise reorder_greedy() with arbitrary input (not chosen for any specific reason)
        """
        inputs = [#self.glyph,
            #self.makeGlyphFromText("""
            #    C17,2638,6563,2,END
            #    C13,END
            #    C17,2679,6558,2,END
            #    C17,2677,6569,2,END
            #    C17,2663,6573,2,END
            #    C14,END
            #    """),
            #self.makeGlyphFromText("""
            #    C17,2675,6524,2,END
            #    C13,END
            #    C17,2686,6491,2,END
            #    C17,2698,6485,2,END
            #    C17,2706,6495,2,END
            #    C17,2697,6502,2,END
            #    C17,2690,6509,2,END
            #    C17,2688,6510,2,END
            #    C17,2675,6524,2,END
            #    C14,END
            #    """),
            #self.makeGlyphFromText("""
            #    C17,2644,6558,2,END
            #    C13,END
            #    C17,2647,6544,2,END
            #    C17,2665,6542,2,END
            #    C17,2661,6556,2,END
            #    C17,2660,6557,2,END
            #    C17,2644,6558,2,END
            #    C14,END
            #    """),
            #self.makeGlyphFromText("""
            #    C17,2638,6563,2,END
            #    C13,END
            #    C17,2679,6558,2,END
            #    C17,2677,6569,2,END
            #    C17,2663,6573,2,END
            #    C14,END
            #    C17,2726,6599,2,END
            #    C13,END
            #    """),
            #self.makeGlyphFromText("""
            #    C17,2675,6524,2,END
            #    C13,END
            #    C17,2686,6491,2,END
            #    C17,2698,6485,2,END
            #    C17,2706,6495,2,END
            #    C17,2697,6502,2,END
            #    C17,2690,6509,2,END
            #    C17,2688,6510,2,END
            #    C17,2675,6524,2,END
            #    C14,END
            #    """),
            self.makeGlyphFromText("""
                C17,5897,3692,2,END
                C13,END
                C17,5899,3690,2,END
                C17,5900,3688,2,END
                C17,5894,3695,2,END
                C17,5897,3692,2,END
                C14,END
                """),
            self.makeGlyphFromText("""
                C17,5827,3665,2,END
                C13,END
                C17,5828,3663,2,END
                C17,5829,3661,2,END
                C17,5832,3657,2,END
                C17,5835,3655,2,END
                C17,5828,3666,2,END
                C17,5827,3666,2,END
                C17,5827,3665,2,END
                C14,END
                """),
            self.makeGlyphFromText("""
                C17,5820,3651,2,END
                C13,END
                C17,5821,3649,2,END
                C17,5822,3647,2,END
                C17,5822,3645,2,END
                C17,5816,3656,2,END
                C17,5820,3651,2,END
                C14,END
                """),
            self.makeGlyphFromText("""
                C17,5825,3624,2,END
                C13,END
                C17,5824,3623,2,END
                C17,5823,3624,2,END
                C17,5822,3625,2,END
                C17,5821,3626,2,END
                C17,5825,3624,2,END
                C14,END
                """),
            self.makeGlyphFromText("""
                C17,5841,3622,2,END
                C13,END
                C17,5841,3621,2,END
                C17,5841,3620,2,END
                C17,5838,3619,2,END
                C17,5833,3618,2,END
                C17,5837,3625,2,END
                C17,5838,3625,2,END
                C17,5839,3625,2,END
                C17,5841,3623,2,END
                C17,5841,3622,2,END
                C14,END
                """),
            self.makeGlyphFromText("""
                C17,5793,3601,2,END
                C13,END
                C17,5789,3594,2,END
                C17,5782,3576,2,END
                C17,5780,3568,2,END
                C17,5797,3609,2,END
                C17,5794,3605,2,END
                C17,5793,3601,2,END
                C14,END
                """),
            ]

        ordered = reorder_greedy(inputs)

        #print('inputs : {}'.format([g1.distance_to(g2) for (g1, g2) in pairwise(inputs)]))
        #print('ordered: {}'.format([g1.distance_to(g2) for (g1, g2) in pairwise(ordered)]))

        self.assertEqual(ordered[0], inputs[0])
        self.assertLessEqual(ordered[0].distance_to(ordered[1]), inputs[0].distance_to(ordered[2]))

    def test_pruned_instructions(self):
        glyphs = [
            self.makeGlyphFromText("""
                C17,5841,3622,2,END
                C13,END
                C17,5838,3619,2,END
                C14,END
            """),
            self.makeGlyphFromText("""
                C17,5838,3619,2,END
                C13,END
                C17,5782,3576,2,END
                C14,END
            """),
        ]
        instructions = iter_instructions(glyphs)
        pruned = prune_zero_distance_penups(instructions)
        lines = '\n'.join([i.line for i in pruned])
        self.assertEqual(lines,
            "C14,END\n"
            "C17,5841,3622,2,END\n"
            "C13,END\n"
            "C17,5838,3619,2,END\n"
            "C17,5782,3576,2,END\n"
            "C14,END")

    def test_three_continuing_glyphs(self):
        glyphs = [
            self.makeGlyphFromText("""
                C17,5841,3622,2,END
                C13,END
                C17,5838,3619,2,END
                C14,END
            """),
            self.makeGlyphFromText("""
                C17,5838,3619,2,END
                C13,END
                C17,5782,3576,2,END
                C14,END
            """),
            self.makeGlyphFromText("""
                C17,5782,3576,2,END
                C13,END
                C17,5700,3600,2,END
                C14,END
            """),
        ]
        instructions = iter_instructions(glyphs)
        pruned = prune_zero_distance_penups(instructions)
        lines = '\n'.join([i.line for i in pruned])
        self.assertEqual(lines,
            "C14,END\n"
            "C17,5841,3622,2,END\n"
            "C13,END\n"
            "C17,5838,3619,2,END\n"
            "C17,5782,3576,2,END\n"
            "C17,5700,3600,2,END\n"
            "C14,END")

    def test_distance_to(self):
        one = self.makeGlyphFromText("""
                C17,5782,3576,2,END
                C13,END
                C17,5700,3600,2,END
                C14,END
            """)
            
        two = self.makeGlyphFromText("""
                C17,5838,3619,2,END
                C13,END
                C17,5782,3576,2,END
                C14,END
            """)

        three = self.makeGlyphFromText("""
                C17,5701,3619,2,END
                C13,END
                C17,5782,3576,2,END
                C14,END
            """)

        # one -> two == max(5838-5700, 3619-3600)
        # one -> two_reversed == max(...

        self.assertEqual(one.distance_to(two), one._distance_to_slow(two))
        self.assertEqual(two.distance_to(one), two._distance_to_slow(one))
        self.assertEqual(one.distance_to_if_other_reversed(two),
            one._distance_to_if_other_reversed_slow(two))
        self.assertEqual(two.distance_to_if_other_reversed(one),
            two._distance_to_if_other_reversed_slow(one))

        self.assertEqual(three.distance_to(two), three._distance_to_slow(two))
        self.assertEqual(two.distance_to(three), two._distance_to_slow(three))
        self.assertEqual(three.distance_to_if_other_reversed(two),
            three._distance_to_if_other_reversed_slow(two))
        self.assertEqual(two.distance_to_if_other_reversed(three),
            two._distance_to_if_other_reversed_slow(three))

        self.assertEqual(one.distance_to(three), one._distance_to_slow(three))
        self.assertEqual(three.distance_to(one), three._distance_to_slow(one))
        self.assertEqual(one.distance_to_if_other_reversed(three),
            one._distance_to_if_other_reversed_slow(three))
        self.assertEqual(three.distance_to_if_other_reversed(one),
            three._distance_to_if_other_reversed_slow(one))


if __name__ == '__main__':
    unittest.main()
