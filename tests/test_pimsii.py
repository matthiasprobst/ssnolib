import json
import unittest

from ssnolib import StandardName
from ssnolib.pimsii import Property
from ssnolib.pimsii.variable import Variable


class TestPIMSII(unittest.TestCase):

    def testVariable(self):
        variable = Variable(
            id="_:b1",
            label="my variable"
        )
        self.assertDictEqual(
            {
                "@context": {
                    "owl": "http://www.w3.org/2002/07/owl#",
                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                    "pims": "http://www.molmod.info/semantics/pims-ii.ttl#",
                    "m4i": "http://w3id.org/nfdi4ing/metadata4ing#",
                    "skos": "http://www.w3.org/2004/02/skos/core#",
                    "ssno": "https://matthiasprobst.github.io/ssno#",
                    "schema": "https://schema.org/",
                    "dcterms": "http://purl.org/dc/terms/",
                },
                "@type": "pims:Variable",
                "rdfs:label": "my variable",
                "@id": "_:b1"
            },
            json.loads(variable.model_dump_jsonld())
        )

    def testProperty(self):
        self.maxDiff = None
        prop = Property(
            id="_:b1",
            label="my property",
            hasValue=5.4,
            hasStandardName=StandardName(
                id="_:b2",
                standardName='x_velocity',
                unit='m/s')
        )
        self.assertDictEqual(
            {
                "@context": {
                    "owl": "http://www.w3.org/2002/07/owl#",
                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                    "pims": "http://www.molmod.info/semantics/pims-ii.ttl#",
                    "m4i": "http://w3id.org/nfdi4ing/metadata4ing#",
                    "ssno": "https://matthiasprobst.github.io/ssno#",
                    "skos": "http://www.w3.org/2004/02/skos/core#",
                    "dcterms": "http://purl.org/dc/terms/",
                    "schema": "https://schema.org/",
                    "dcat": "http://www.w3.org/ns/dcat#"
                },
                "@type": "pims:Property",
                "rdfs:label": "my property",
                "m4i:hasValue": 5.4,
                "ssno:hasStandardName": {
                    "@type": "ssno:StandardName",
                    "ssno:standardName": "x_velocity",
                    "ssno:unit": {"@id": "http://qudt.org/vocab/unit/M-PER-SEC"},
                    "@id": "_:b2"
                },
                "@id": "_:b1"
            },
            json.loads(prop.model_dump_jsonld())
        )
