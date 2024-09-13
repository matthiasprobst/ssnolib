import pathlib
import unittest

from ssnolib.utils import gpfqcs

__this_dir__ = pathlib.Path(__file__).parent


class TestVersion(unittest.TestCase):

    def test_gpfqcs(self):
        # Test with the given example
        input_str = "[component] standard_name [in_medium]"
        positions = gpfqcs(input_str)
        self.assertDictEqual(
            {-1: 'component', 1: 'in_medium'},
            positions
        )

        input_str = "[surface][component] standard_name [surface] [medium] [process] [condition]"
        positions = gpfqcs(input_str)
        self.assertDictEqual(
            {-2: 'surface', -1: 'component', 1: 'surface', 2: 'medium', 3: "process", 4: "condition"},
            positions
        )
