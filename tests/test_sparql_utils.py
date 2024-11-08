import pathlib
import unittest

__this_dir__ = pathlib.Path(__file__).parent

from ssnolib.sparql_utils import build_simple_sparql_query, WHERE
import rdflib


class TestSparqlUtils(unittest.TestCase):

    def test_build_sparql_query(self):
        sparql_query = build_simple_sparql_query(dict(
            owl="https://www.w3.org/2002/07/owl#",
            rdfs="http://www.w3.org/2000/01/rdf-schema#"
        ),
            wheres=[WHERE(s="?id", p="a", o="ssno:StandardNameTable")]
        )
        expected_sparql_string = """PREFIX owl: <https://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?id
WHERE {?id a ssno:StandardNameTable .
}"""
        self.assertEqual(expected_sparql_string, sparql_query.query_string)

    def test_perform_simple_query(self):
        test_data = """
{
    "@context": {
        "hdf5": "http://purl.allotrope.org/ontologies/hdf5/1.8#",
        "m4i": "http://w3id.org/nfdi4ing/metadata4ing#",
        "ssno": "https://matthiasprobst.github.io/ssno#"
    },
    "@graph": [
        {
            "@id": "_:N139",
            "@type": "hdf5:File",
            "hdf5:rootGroup": {
                "@id": "_:N138",
                "@type": [
                    "hdf5:Group",
                    "https://www.wikidata.org/wiki/Q1058834"
                ],
                "hdf5:attribute": [
                    {
                        "@id": "_:N140",
                        "@type": "hdf5:Attribute",
                        "hdf5:name": "fan_type",
                        "hdf5:value": "centrifugal"
                    },
                    {
                        "@id": "_:N141",
                        "@type": "hdf5:Attribute",
                        "hdf5:name": "manufacturing_method",
                        "hdf5:value": "rapid_prototyping"
                    }
                ]
            }
        }
    ]
}
    """
        spql = build_simple_sparql_query(
            prefixes={
                "ssno": "https://matthiasprobst.github.io/ssno#",
                "hdf5": "http://purl.allotrope.org/ontologies/hdf5/1.8#"
            },
            wheres=[
                WHERE("?id", "a", "hdf5:Attribute"),
                WHERE("?id", "hdf5:value", "\"centrifugal\"")
            ]
        )
        g = rdflib.Graph()
        g.parse(data=test_data,
                format='json-ld',
                context={
                    "ssno": "https://matthiasprobst.github.io/ssno#",
                    "hdf5": "http://purl.allotrope.org/ontologies/hdf5/1.8#"
                })
        res = spql.query(g)
        print(res)
