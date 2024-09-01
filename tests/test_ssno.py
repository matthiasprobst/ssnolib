import json
import pathlib
import unittest

import h5rdmtoolbox as h5tbx
import ontolutils
import requests.exceptions
import yaml
from ontolutils import QUDT_UNIT

import ssnolib
from ssnolib import StandardName, StandardNameTable
from ssnolib.dcat import Distribution
from ssnolib.qudt import parse_unit

# ignore User Warnings:

__this_dir__ = pathlib.Path(__file__).parent
CACHE_DIR = ssnolib.utils.get_cache_dir()

SNT_JSONLD = """{
  "@context": {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "prov": "http://www.w3.org/ns/prov#",
    "ssnolib": "https://matthiasprobst.github.io/ssno#"
  },
  "@type": "ssnolib:StandardNameTable",
  "dct:title": "OpenCeFaDB Fan Standard Name Table",
  "ssnolib:standard_names": [
    {
      "@type": "ssnolib:StandardName",
      "ssnolib:standard_name": "absolute_pressure",
      "dcterms:description": "Pressure is force per unit area. Absolute air pressure is pressure deviation to a total vacuum.",
      "canonical_units": "Pa",
      "@id": "local:39257b94-d31c-480e-a43c-8ae7f57fae6d"
    },
    {
      "@type": "ssnolib:StandardName",
      "ssnolib:standard_name": "ambient_static_pressure",
      "dcterms:description": "Static air pressure is the amount of pressure exerted by air that is not moving. Ambient static air pressure is the static air pressure of the surrounding air.",
      "canonical_units": "Pa",
      "@id": "local:0637ec26-310b-4b0a-bf4c-e51d4afccc7d"
    },
    {
      "@type": "ssnolib:StandardName",
      "ssnolib:standard_name": "ambient_temperature",
      "dcterms:description": "Air temperature is the bulk temperature of the air, not the surface (skin) temperature. Ambient air temperature is the temperature of the surrounding air.",
      "canonical_units": "K",
      "@id": "local:3286d041-a826-4776-9d25-065dae107b55"
    },
    {
      "@type": "ssnolib:StandardName",
      "ssnolib:standard_name": "auxiliary_fan_rotational_speed",
      "dcterms:description": "Number of revolutions of an auxiliary fan.",
      "canonical_units": "1/s",
      "@id": "local:2a521e9d-4481-4965-9b42-390db2da4c83"
    }
  ]
}"""


class TestSSNO(unittest.TestCase):

    def tearDown(self):
        pathlib.Path('snt.json').unlink(missing_ok=True)
        pathlib.Path('snt.yaml').unlink(missing_ok=True)
        pathlib.Path('snt2.yaml').unlink(missing_ok=True)

    def test_standard_name(self):
        sn = StandardName(standard_name='x_velocity',
                          description='x component of velocity',
                          canonical_units=QUDT_UNIT.M_PER_SEC)  # 'm s-1'
        self.assertIsInstance(sn, ontolutils.Thing)
        self.assertIsInstance(sn, StandardName)
        self.assertEqual(sn.standard_name, 'x_velocity')
        self.assertEqual(sn.description, 'x component of velocity')
        self.assertEqual(sn.canonical_units, str(parse_unit('m s-1')))

        sn = StandardName(standard_name='x_velocity',
                          description='x component of velocity',
                          canonical_units='m s-1')
        self.assertEqual(sn.canonical_units, str(parse_unit('m s-1')))

        with open('sn.jsonld', 'w') as f:
            f.write(sn.model_dump_jsonld())

        sn_loaded = ontolutils.query(StandardName, source='sn.jsonld')
        self.assertEqual(len(sn_loaded), 1)
        self.assertEqual(sn_loaded[0].standard_name, 'x_velocity')
        self.assertEqual(sn_loaded[0].description, 'x component of velocity')
        self.assertEqual(sn_loaded[0].canonical_units, str(parse_unit('m s-1')))

        sn_loaded = StandardName.from_jsonld(data=sn.model_dump_jsonld())
        self.assertEqual(len(sn_loaded), 1)
        self.assertEqual(sn_loaded[0].standard_name, 'x_velocity')
        self.assertEqual(sn_loaded[0].description, 'x component of velocity')
        self.assertEqual(sn_loaded[0].canonical_units, str(parse_unit('m s-1')))

        pathlib.Path('sn.jsonld').unlink(missing_ok=True)

    def test_standard_name_with_table(self):
        snt = StandardNameTable(identifier='https://doi.org/10.5281/zenodo.10428817')

        xvel = StandardName(
            standard_name_table=snt
        )
        self.assertEqual(xvel.__str__(), '')
        self.assertEqual(xvel.standard_name_table, snt)

    def test_standard_name_table(self):
        sn1 = StandardName(standard_name='x_velocity',
                           description='x component of velocity',
                           canonical_units='m s-1')
        sn2 = StandardName(standard_name='y_velocity',
                           description='y component of velocity',
                           canonical_units='m s-1')

        snt = StandardNameTable(standard_names=[sn1, sn2])
        with open('snt.json', 'w') as f:
            f.write(snt.model_dump_jsonld())

        snt_loaded = list(StandardNameTable.from_jsonld(data=snt.model_dump_jsonld(), limit=None))
        self.assertEqual(len(snt_loaded), 1)
        self.assertEqual(len(snt_loaded[0].standard_names), 2)
        self.assertEqual(snt_loaded[0].standard_names[0].standard_name, 'x_velocity')
        self.assertEqual(snt_loaded[0].standard_names[0].description, 'x component of velocity')
        self.assertEqual(snt_loaded[0].standard_names[0].canonical_units, str(parse_unit('m s-1')))
        self.assertEqual(snt_loaded[0].standard_names[1].standard_name, 'y_velocity')
        self.assertEqual(snt_loaded[0].standard_names[1].description, 'y component of velocity')
        self.assertEqual(snt_loaded[0].standard_names[1].canonical_units, str(parse_unit('m s-1')))

        snt_loaded = StandardNameTable.from_jsonld(data=snt.model_dump_jsonld(), limit=1)
        self.assertEqual(len(snt_loaded.standard_names), 2)
        self.assertEqual(snt_loaded.standard_names[0].standard_name, 'x_velocity')
        self.assertEqual(snt_loaded.standard_names[0].description, 'x component of velocity')
        self.assertEqual(snt_loaded.standard_names[0].canonical_units, str(parse_unit('m s-1')))
        self.assertEqual(snt_loaded.standard_names[1].standard_name, 'y_velocity')
        self.assertEqual(snt_loaded.standard_names[1].description, 'y component of velocity')
        self.assertEqual(snt_loaded.standard_names[1].canonical_units, str(parse_unit('m s-1')))
        pathlib.Path('snt.json').unlink(missing_ok=True)

    def test_standard_name_table_from_jsonld(self):
        snt_jsonld_filename = pathlib.Path(__this_dir__, 'snt.json')
        with open(snt_jsonld_filename, 'w') as f:
            json.dump(json.loads(SNT_JSONLD), f)
        snt = StandardNameTable.parse(snt_jsonld_filename, fmt='jsonld')

        snt_jsonld_filename.unlink(missing_ok=True)
        self.assertEqual(snt.title, 'OpenCeFaDB Fan Standard Name Table')

    def test_standard_name_table_from_yaml(self):
        pathlib.Path('snt.yaml').unlink(missing_ok=True)

        dist = Distribution(downloadURL='http://example.org/snt.yaml',
                            mediaType='application/yaml')
        snt = StandardNameTable()
        with self.assertRaises(requests.exceptions.HTTPError):
            snt.parse(dist)

        snt_yaml_data = {'name': 'SNT',
                         'description': 'A testing SNT',
                         'version': 'abc123invalid',  # v1.0.0
                         'identifier': 'https://example.org/sntIdentifier',
                         'standard_names': {'x_velocity': {'description': 'x component of velocity',
                                                           'canonical_units': 'm s-1'},
                                            'y_velocity': {'description': 'y component of velocity',
                                                           'canonical_units': 'm s-1'}}}
        with open('snt.yaml', 'w') as f:
            yaml.dump(snt_yaml_data, f)
        snt = StandardNameTable.parse('snt.yaml', fmt='yaml')
        self.assertEqual(snt.title, 'SNT')

        snt = StandardNameTable.parse('snt.yaml', fmt=None)
        self.assertEqual(snt.title, 'SNT')

    def test_standard_name_table_from_xml(self):
        from ssnolib.utils import download_file
        cf_contention = 'http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml'
        snt_xml_filename = download_file(cf_contention,
                                         dest_filename='snt.xml',
                                         exist_ok=True)
        self.assertTrue(snt_xml_filename.exists())

        xml_snt = StandardNameTable.parse(snt_xml_filename, fmt=None)
        self.assertEqual(
            xml_snt.creator.mbox,
            'support@ceda.ac.uk')

        snt_xml_filename = download_file(cf_contention,
                                         dest_filename='snt.xml',
                                         exist_ok=True)
        self.assertTrue(snt_xml_filename.exists())

        snt_xml_filename = download_file(cf_contention,
                                         dest_filename='snt.xml',
                                         exist_ok=True)
        snt_xml_filename.unlink(missing_ok=True)
        snt_xml_filename = download_file(cf_contention)

        snt = StandardNameTable.parse(snt_xml_filename, fmt='xml')
        self.assertEqual(
            snt.creator.mbox,
            'support@ceda.ac.uk')
        snt_xml_filename.unlink(missing_ok=True)

        dist = Distribution(
            downloadURL='http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
            mediaType='application/xml')

        snt = StandardNameTable.parse(dist)
        self.assertEqual(
            snt.creator.mbox,
            'support@ceda.ac.uk'
        )
        self.assertEqual(snt.title, 'cf-standard-name-table')
        pathlib.Path(f'{snt.title}.xml').unlink(missing_ok=True)

    def test_standard_name_table_to_yamL(self):
        snt_yaml_filename = pathlib.Path('snt.yaml')
        if not snt_yaml_filename.exists():
            self.test_standard_name_table_from_yaml()
        assert snt_yaml_filename.exists()
        snt = StandardNameTable.parse(snt_yaml_filename, fmt='yaml')
        snt.to_yaml('snt2.yaml', overwrite=True)

        with open('snt.yaml') as f:
            yaml1 = yaml.safe_load(f)
            for k, v in yaml1.copy()['standard_names'].items():
                print(yaml1["standard_names"][k])
                yaml1['standard_names'][k]['canonical_units'] = str(parse_unit(v['canonical_units']))

        with open('snt2.yaml') as f:
            yaml2 = yaml.safe_load(f)

        self.assertDictEqual(yaml1, yaml2)

    def test_hdf5_accessor(self):
        # noinspection PyUnresolvedReferences
        from ssnolib import h5accessor
        with h5tbx.File() as h5:
            h5.create_dataset('u', data=4.3, attrs={'standard_name': 'x_velocity'})
            with self.assertRaises(ValueError):
                h5.ssno.enrich_hdf()

            h5.attrs['snt'] = 'https://doi.org/10.5281/zenodo.10428817'
            h5.ssno.enrich_hdf(standard_name_table_attribute='snt')
            self.assertEqual(h5.u.rdf.predicate['standard_name'],
                             'https://matthiasprobst.github.io/ssno#hasStandardName')
            self.assertEqual(h5.rdf.predicate['snt'],
                             'https://matthiasprobst.github.io/ssno#hasStandardNameTable')
