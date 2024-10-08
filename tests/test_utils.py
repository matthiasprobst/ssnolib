import pathlib
import unittest
from dataclasses import dataclass

from numpy.ma.testutils import assert_equal

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

    def test_build_sparql_query(self):
        from ssnolib.utils import build_simple_sparql_query, WHERE

        sparql_query = build_simple_sparql_query(dict(
            owl="http://www.w3.org/2002/07/owl#",
            rdfs="http://www.w3.org/2000/01/rdf-schema#"
        ),
            wheres=[WHERE(s="?id", p="a", o="ssno:StandardNameTable")]
        )
        expected_sparql_string = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?id
WHERE {?id a ssno:StandardNameTable .
}"""
        self.assertEqual(expected_sparql_string, sparql_query.query_string)
