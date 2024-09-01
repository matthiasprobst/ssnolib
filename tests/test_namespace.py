import unittest

from rdflib import URIRef

from ssnolib.namespace import SSNO


class TestNamespace(unittest.TestCase):

    def test_namespace(self):
        self.assertIsInstance(SSNO.has_standard_names, URIRef)
        self.assertEqual(SSNO.has_standard_names, URIRef('https://matthiasprobst.github.io/ssno#has_standard_names'))
        self.assertEqual(SSNO.standardNames, URIRef('https://matthiasprobst.github.io/ssno#standardNames'))
        self.assertEqual(SSNO.StandardNames, URIRef('https://matthiasprobst.github.io/ssno#StandardNames'))
