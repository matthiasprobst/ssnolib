import unittest

from ssnolib.ssno.unit_utils import _parse_unit, _get_ureg


class TestUnitParsing(unittest.TestCase):

    def test_malformed_unit(self):
        self.assertEqual(
            _parse_unit("m2/s3"),
            _get_ureg()("m**2/s**3").u
        )

    def test_malformed_unit2(self):
        self.assertEqual(
            _parse_unit("kg m-1 s-1"),
            _get_ureg()("kg/m/s").u
        )
