import json
import pathlib
import unittest
import warnings

import pydantic
import rdflib

import ssnolib
from ssnolib import dcat

__this_dir__ = pathlib.Path(__file__).parent
CACHE_DIR = ssnolib.utils.get_cache_dir()


def _delete_test_data():
    for _filename_to_delete in (CACHE_DIR / 'cf-standard-name-table.xml',
                                CACHE_DIR / 'cfsnt.json',
                                CACHE_DIR / 'cf_table.json',
                                CACHE_DIR / 'cfsnt.json',
                                CACHE_DIR / 'test_snt.yaml',
                                CACHE_DIR / 'cf-standard-name-table.xml',):
        _filename_to_delete.unlink(missing_ok=True)


class TestClasses(unittest.TestCase):

    def setUp(self) -> None:
        warnings.filterwarnings("ignore", category=UserWarning)
        _delete_test_data()

    def tearDown(self) -> None:
        _delete_test_data()

    def test_Organization(self):
        orga = ssnolib.Organization(name='My Orga')
        self.assertEqual(orga.name, 'My Orga')
        orga2 = ssnolib.Organization(name='My Orga', mbox='my.orga@orga.org')
        self.assertEqual(orga2.name, 'My Orga')
        self.assertEqual(str(orga2.mbox), 'my.orga@orga.org')
        self.assertNotEqual(orga, orga2)
        self.assertEqual(orga, orga)

    def test_Person(self):
        contact = ssnolib.Person(mbox='johndoe@email.com')
        self.assertEqual(str(contact.mbox), 'johndoe@email.com')

        contact = ssnolib.Person(firstName='John', lastName='Doe')
        self.assertEqual(contact.firstName, 'John')
        self.assertEqual(contact.lastName, 'Doe')

        # check aliases:
        contact_alias = ssnolib.Person(first_name="John", last_name="Doe")
        self.assertEqual(contact_alias.firstName, 'John')
        self.assertEqual(contact_alias.first_name, 'John')
        self.assertEqual(contact_alias.lastName, 'Doe')
        self.assertEqual(contact_alias.last_name, 'Doe')

    def test_ssnolib_Distribution(self):
        distribution = ssnolib.dcat.Distribution(title='XML Table',
                                                 downloadURL='https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
                                                 mediaType='text/csv')
        self.assertEqual(str(distribution.mediaType),
                         "https://www.iana.org/assignments/media-types/text/csv")

        distribution = ssnolib.dcat.Distribution(title='XML Table',
                                                 downloadURL='https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
                                                 mediaType='application/xml')
        self.assertEqual(str(distribution.mediaType),
                         "https://www.iana.org/assignments/media-types/application/xml")
        self.assertEqual(distribution.title, 'XML Table')
        self.assertEqual(str(distribution.downloadURL),
                         'https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml')

        download_filename = distribution.download('cf-standard-name-table.xml')
        self.assertIsInstance(download_filename, pathlib.Path)
        self.assertTrue(download_filename.exists())
        self.assertTrue(download_filename.is_file())
        download_filename.unlink(missing_ok=True)

    def test_standard_name_table(self):
        snt = ssnolib.StandardNameTable(title='CF Standard Name Table v79')
        self.assertEqual(snt.title, 'CF Standard Name Table v79')
        self.assertEqual(str(snt), 'CF Standard Name Table v79')
        self.assertEqual(repr(snt),
                         f'StandardNameTable(id={snt.id}, title=CF Standard Name Table v79, standardNames=[])')

        distribution = ssnolib.dcat.Distribution(title='XML Table',
                                                 downloadURL='https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
                                                 mediaType='application/xml')
        self.assertEqual(distribution.title, 'XML Table')
        self.assertEqual(str(distribution.downloadURL),
                         'https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml')
        snt = ssnolib.StandardNameTable(title='CF Standard Name Table v79',
                                        distribution=[distribution, ])
        self.assertEqual(snt.distribution[0].title, 'XML Table')
        self.assertEqual(str(snt.distribution[0].downloadURL),
                         'https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml')
        table_filename = snt.distribution[0].download(
            dest_filename=CACHE_DIR / 'cf-standard-name-table.xml',
        )
        self.assertIsInstance(table_filename, pathlib.Path)
        self.assertTrue(table_filename.exists())
        self.assertTrue(table_filename.is_file())
        self.assertEqual(table_filename, CACHE_DIR / 'cf-standard-name-table.xml')
        try:
            snt.distribution[0].download(
                dest_filename=CACHE_DIR / 'cf-standard-name-table.xml',
            )
        except FileExistsError:
            pass
        snt.distribution[0].download(
            dest_filename=CACHE_DIR / 'cf-standard-name-table.xml',
            overwrite_existing=True
        )
        snt_from_xml = snt.parse(table_filename, fmt='xml', make_standard_names_lowercase=True)
        self.assertIsInstance(snt_from_xml.standardNames, list)
        for sn in snt_from_xml.standardNames:
            self.assertIsInstance(sn, ssnolib.StandardName)

        snt_from_xml_dict = snt_from_xml.model_dump(exclude_none=True)

        agent = snt_from_xml_dict['qualifiedAttribution']["agent"]
        agent.pop("id")
        self.assertDictEqual(agent,
                             {'mbox': 'support@ceda.ac.uk',
                              'name': 'Centre for Environmental Data Analysis'})

        with self.assertRaises(pydantic.ValidationError):
            # invalid string for title:
            ssnolib.StandardNameTable(title=123)

        snt_from_xml.title = f'CF Standard Name Table {snt_from_xml.version}'
        with open(CACHE_DIR / 'cfsnt.json', 'w', encoding='utf-8') as f:
            f.write(snt_from_xml.model_dump_jsonld(context=None))

        g = rdflib.Graph().parse(CACHE_DIR / 'cfsnt.json', format='json-ld')
        for s, p, o in g.triples((None, None, None)):
            self.assertIsInstance(p, rdflib.URIRef)

        snt.model_dump_jsonld()

    def test_standard_name(self):
        """describe "air_temperature" from
        https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html"""

        with self.assertRaises(pydantic.ValidationError):
            # invalid unit
            ssnolib.StandardName(
                standardName='air_temperature',
                unit=123,
                description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.', )

        atemp = ssnolib.StandardName(
            standardName='air_temperature',
            unit='K',
            description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')

        self.assertEqual(str(atemp), 'air_temperature')
        self.assertEqual(atemp.standardName, 'air_temperature')
        self.assertEqual(atemp.unit, 'http://qudt.org/vocab/unit/K')
        self.assertEqual(atemp.description,
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')

        self.assertEqual(str(atemp), 'air_temperature')
        self.assertEqual(atemp.standardNameTable, None)

        # to dict:
        atemp_dict = atemp.model_dump(exclude_none=True)
        self.assertIsInstance(atemp_dict, dict)
        self.assertEqual(atemp_dict['standardName'], 'air_temperature')
        self.assertEqual(atemp_dict['unit'], 'http://qudt.org/vocab/unit/K')
        self.assertEqual(atemp_dict['description'],
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')

        atemp_json = atemp.model_dump_json()
        self.assertIsInstance(atemp_json, str)
        atemp_json_dict = json.loads(atemp_json)
        self.assertIsInstance(atemp_json_dict, dict)
        self.assertEqual(atemp_json_dict['standardName'], 'air_temperature')
        self.assertEqual(atemp_json_dict['unit'], 'http://qudt.org/vocab/unit/K')
        self.assertEqual(atemp_json_dict['description'],
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')

        # to json-ld:
        jsonld_string = atemp.model_dump_jsonld()

        with open(CACHE_DIR / 'cf_table.json', 'w') as f:
            f.write(jsonld_string)

        g = rdflib.Graph()
        g.parse(data=jsonld_string, format='json-ld')
        self.assertEqual(len(g), 4)
        for s, p, o in g:
            self.assertIsInstance(s, rdflib.BNode)
            self.assertIsInstance(p, rdflib.URIRef)
            self.assertIsInstance(o, str)

        # serialize with rdflib:
        jsonld_dict = json.loads(jsonld_string)
        # self.assertEqual(jsonld_dict['@context']['@import'], CONTEXT)

        self.assertEqual(jsonld_dict['@type'], 'ssno:StandardName')
        self.assertEqual(jsonld_dict['ssno:standardName'], 'air_temperature')
        self.assertEqual(jsonld_dict['ssno:description'],
                         'Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')
        self.assertEqual(jsonld_dict['ssno:unit'], 'http://qudt.org/vocab/unit/K')

        # http://qudt.org/vocab/unit/K

    def test_snt_from_yaml(self):
        snt_yml_filename = __this_dir__ / 'data/test_snt.yaml'
        distribution = dcat.Distribution(title='XML Table',
                                         downloadURL=f'file:///{snt_yml_filename}',
                                         mediaType='application/yaml')
        filename = distribution.download(CACHE_DIR / 'test_snt.yaml')
        self.assertNotEqual(filename, snt_yml_filename)
        self.assertTrue(pathlib.Path(filename).exists())
        self.assertIsInstance(filename, pathlib.Path)
        snt = ssnolib.StandardNameTable(
            title='Yaml Test SNT',
            distribution=[distribution, ]
        )
        snt.parse(snt.distribution[0])
