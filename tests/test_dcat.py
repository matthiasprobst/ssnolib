import pathlib
import unittest

import requests.exceptions

import ssnolib
import utils
from ssnolib import dcat, prov, foaf
import sys
__this_dir__ = pathlib.Path(__file__).parent

CACHE_DIR = ssnolib.utils.get_cache_dir()

def get_python_version():
    """Get the current Python version as a tuple."""
    return sys.version_info.major, sys.version_info.minor, sys.version_info.micro

class TestDcat(utils.ClassTest):

    def test_Resource(self):
        resource1 = dcat.Resource(
            title='Resource title',
            description='Resource description',
            creator=prov.Person(first_name='John', lastName='Doe'),
            version='1.0',
            identifier='https://example.com/resource'
        )
        self.assertEqual(resource1.id, 'https://example.com/resource')
        self.assertEqual(resource1.title, 'Resource title')
        self.assertEqual(resource1.description, 'Resource description')
        self.assertIsInstance(resource1.creator, prov.Person)
        self.assertEqual(resource1.creator.firstName, 'John')
        self.assertEqual(resource1.creator.lastName, 'Doe')
        self.assertEqual(resource1.version, '1.0')
        self.assertEqual(str(resource1.identifier), 'https://example.com/resource')

    @unittest.skipIf(condition=9 < get_python_version()[1] < 13,
                         reason="Only testing on min and max python version")
    def test_Distribution(self):
        distribution_none_downloadURL = dcat.Distribution(
            id='_:b2',
            title='Distribution title',
            description='Distribution description'
        )
        self.assertEqual(distribution_none_downloadURL.id, '_:b2')
        with self.assertRaises(ValueError):
            distribution_none_downloadURL.download()

        distribution_wrongfile = dcat.Distribution(
            title='Distribution title',
            description='Distribution description',
            downloadURL='file://path/invalid.txt'
        )
        with self.assertRaises(FileNotFoundError):
            distribution_wrongfile.download()

        distribution1 = dcat.Distribution(
            title='Distribution title',
            description='Distribution description',
            creator=prov.Person(first_name='John', lastName='Doe'),
            version='1.0',
            identifier='https://example.com/distribution',
            accessURL='https://example.com/distribution',
            downloadURL='https://example.com/distribution/download'
        )
        self.assertEqual(distribution1.id, 'https://example.com/distribution')
        self.assertEqual(distribution1.title, 'Distribution title')
        self.assertEqual(distribution1.description, 'Distribution description')
        self.assertIsInstance(distribution1.creator, prov.Person)
        self.assertEqual(distribution1.creator.firstName, 'John')
        self.assertEqual(distribution1.creator.lastName, 'Doe')
        self.assertEqual(distribution1.version, '1.0')
        self.assertEqual(str(distribution1.identifier), 'https://example.com/distribution')
        self.assertEqual(str(distribution1.accessURL), 'https://example.com/distribution')
        self.assertEqual(str(distribution1.downloadURL), 'https://example.com/distribution/download')

        # with self.assertRaises((requests.exceptions.HTTPError, requests.exceptions.ConnectionError)):
        #     distribution1.download(timeout=10)

        piv_dist = dcat.Distribution(
            downloadURL=self.test_jsonld_filename
        )
        filename = piv_dist.download(timeout=10)
        self.assertTrue(filename.exists())
        self.assertEqual(filename.name, 'piv_dataset.jsonld')
        self.assertIsInstance(filename, pathlib.Path)

        local_dist = dcat.Distribution(
            downloadURL=filename
        )
        i = 0
        i_max = 3
        while i < i_max:
            try:
                local_filename = local_dist.download(timeout=60)
                break
            except requests.exceptions.HTTPSConnection as e:
                print(e)
                i += 1
        self.assertTrue(local_filename.exists())
        self.assertEqual(local_filename.name, 'piv_dataset.jsonld')
        self.assertIsInstance(local_filename, pathlib.Path)

        filename.unlink(missing_ok=True)

    def test_Dataset(self):
        person = prov.Person(id="https://example.of/123", first_name='John', lastName='Doe')
        dataset1 = dcat.Dataset(
            title='Dataset title',
            description='Dataset description',
            creator=person,
            version='1.0',
            identifier='https://example.com/dataset',
            distribution=[
                dcat.Distribution(
                    title='Distribution title',
                    description='Distribution description',
                    identifier='https://example.com/distribution',
                    accessURL='https://example.com/distribution',
                    downloadURL='https://example.com/distribution/download'
                )
            ]
        )
        self.assertEqual(dataset1.id, 'https://example.com/dataset')
        self.assertEqual(dataset1.identifier, 'https://example.com/dataset')
        self.assertEqual(dataset1.title, 'Dataset title')
        self.assertEqual(dataset1.description, 'Dataset description')
        self.assertIsInstance(dataset1.creator, prov.Person)
        self.assertEqual(dataset1.creator.firstName, 'John')
        self.assertEqual(dataset1.creator.lastName, 'Doe')
        self.assertEqual(dataset1.version, '1.0')
        self.assertEqual(str(dataset1.identifier), 'https://example.com/dataset')
        self.assertIsInstance(dataset1.distribution[0], dcat.Distribution)
        self.assertEqual(dataset1.distribution[0].title, 'Distribution title')
        self.assertEqual(dataset1.distribution[0].description, 'Distribution description')
        self.assertEqual(str(dataset1.distribution[0].id), 'https://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].identifier), 'https://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].accessURL), 'https://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].downloadURL), 'https://example.com/distribution/download')

        ds = dcat.Dataset(
            title='Dataset title',
            description='Dataset description',
            creator=person.id,
            version='1.0',
            identifier='https://example.com/dataset',
            distribution=[
                dcat.Distribution(
                    title='Distribution title',
                    description='Distribution description',
                    identifier='https://example.com/distribution',
                    accessURL='https://example.com/distribution',
                    downloadURL='https://example.com/distribution/download'
                )
            ]
        )
        ttl = ds.serialize("ttl")
        self.assertEqual(ttl, """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://example.com/dataset> a dcat:Dataset ;
    dcterms:creator <https://example.of/123> ;
    dcterms:description "Dataset description" ;
    dcterms:identifier <https://example.com/dataset> ;
    dcterms:title "Dataset title" ;
    dcat:distribution <https://example.com/distribution> ;
    dcat:version "1.0" .

<https://example.com/distribution> a dcat:Distribution ;
    dcterms:description "Distribution description" ;
    dcterms:identifier <https://example.com/distribution> ;
    dcterms:title "Distribution title" ;
    dcat:accessURL <https://example.com/distribution> ;
    dcat:downloadURL <https://example.com/distribution/download> .

""")

    def test_Dataset_with_foaf(self):
        person = foaf.Person(openid="http://example.com/people/johndoe",

                             first_name='John', family_name='Doe')
        self.assertEqual(person.id, 'http://example.com/people/johndoe')
        dataset1 = dcat.Dataset(
            title='Dataset title',
            description='Dataset description',
            creator=person,
            version='1.0',
            identifier='https://example.com/dataset',
            distribution=[
                dcat.Distribution(
                    title='Distribution title',
                    description='Distribution description',
                    identifier='https://example.com/distribution',
                    accessURL='https://example.com/distribution',
                    downloadURL='https://example.com/distribution/download'
                )
            ]
        )
        self.assertEqual(dataset1.id, 'https://example.com/dataset')
        self.assertEqual(dataset1.identifier, 'https://example.com/dataset')
        self.assertEqual(dataset1.title, 'Dataset title')
        self.assertEqual(dataset1.description, 'Dataset description')
        self.assertIsInstance(dataset1.creator, foaf.Person)
        self.assertEqual(dataset1.creator.firstName, 'John')
        self.assertEqual(dataset1.creator.familyName, 'Doe')
        self.assertEqual(dataset1.version, '1.0')
        self.assertEqual(str(dataset1.identifier), 'https://example.com/dataset')
        self.assertIsInstance(dataset1.distribution[0], dcat.Distribution)
        self.assertEqual(dataset1.distribution[0].title, 'Distribution title')
        self.assertEqual(dataset1.distribution[0].description, 'Distribution description')
        self.assertEqual(str(dataset1.distribution[0].id), 'https://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].identifier), 'https://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].accessURL), 'https://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].downloadURL), 'https://example.com/distribution/download')

        dataset2 = dcat.Dataset(
            title='Dataset title',
            description='Dataset description',
            creator=person.id,
            version='1.0',
            identifier='https://example.com/dataset',
            distribution=[
                dcat.Distribution(
                    title='Distribution title',
                    description='Distribution description',
                    identifier='https://example.com/distribution',
                    accessURL='https://example.com/distribution',
                    downloadURL='https://example.com/distribution/download'
                )
            ]
        )
        self.assertEqual(str(dataset2.creator), str(person.id))
