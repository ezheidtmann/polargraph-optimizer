#!/usr/bin/python

from lib import *
import unittest

class TestLib(unittest.TestCase):
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
        self.instructions = []
        for line in lines.split("\n"):
            line = line.strip()
            if len(line):
                self.instructions.append(Instruction(line))

        self.glyph = Glyph(self.instructions)
   
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

if __name__ == '__main__':
    unittest.main()
