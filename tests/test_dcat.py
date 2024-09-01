import pathlib

import requests.exceptions

import ssnolib
import utils
from ssnolib import dcat, prov

__this_dir__ = pathlib.Path(__file__).parent
CACHE_DIR = ssnolib.utils.get_cache_dir()


class TestDcat(utils.ClassTest):

    def test_Resource(self):
        resource1 = dcat.Resource(
            id='_:b1',
            title='Resource title',
            description='Resource description',
            creator=prov.Person(name='John Doe'),
            version='1.0',
            identifier='http://example.com/resource'
        )
        self.assertEqual(resource1.id, '_:b1')
        self.assertEqual(resource1.title, 'Resource title')
        self.assertEqual(resource1.description, 'Resource description')
        self.assertIsInstance(resource1.creator, prov.Person)
        self.assertEqual(resource1.creator.name, 'John Doe')
        self.assertEqual(resource1.version, '1.0')
        self.assertEqual(str(resource1.identifier), 'http://example.com/resource')

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
            id='_:b2',
            title='Distribution title',
            description='Distribution description',
            downloadURL='file://path/invalid.txt'
        )
        with self.assertRaises(FileNotFoundError):
            distribution_wrongfile.download()

        distribution1 = dcat.Distribution(
            id='_:b2',
            title='Distribution title',
            description='Distribution description',
            creator=prov.Person(name='John Doe'),
            version='1.0',
            identifier='http://example.com/distribution',
            accessURL='http://example.com/distribution',
            downloadURL='http://example.com/distribution/download'
        )
        self.assertEqual(distribution1.id, '_:b2')
        self.assertEqual(distribution1.title, 'Distribution title')
        self.assertEqual(distribution1.description, 'Distribution description')
        self.assertIsInstance(distribution1.creator, prov.Person)
        self.assertEqual(distribution1.creator.name, 'John Doe')
        self.assertEqual(distribution1.version, '1.0')
        self.assertEqual(str(distribution1.identifier), 'http://example.com/distribution')
        self.assertEqual(str(distribution1.access_URL), 'http://example.com/distribution')
        self.assertEqual(str(distribution1.download_URL), 'http://example.com/distribution/download')

        with self.assertRaises(requests.exceptions.HTTPError):
            distribution1.download(timeout=60)

        piv_dist = dcat.Distribution(
            downloadURL=self.test_jsonld_filename
        )
        filename = piv_dist.download(timeout=60)
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
        dataset1 = dcat.Dataset(
            id='_:b3',
            title='Dataset title',
            description='Dataset description',
            creator=prov.Person(name='John Doe'),
            version='1.0',
            identifier='http://example.com/dataset',
            distribution=[
                dcat.Distribution(
                    id='_:b4',
                    title='Distribution title',
                    description='Distribution description',
                    creator=prov.Person(name='John Doe'),
                    version='1.0',
                    identifier='http://example.com/distribution',
                    access_URL='http://example.com/distribution',
                    downloadURL='http://example.com/distribution/download'
                )
            ]
        )
        self.assertEqual(dataset1.id, '_:b3')
        self.assertEqual(dataset1.title, 'Dataset title')
        self.assertEqual(dataset1.description, 'Dataset description')
        self.assertIsInstance(dataset1.creator, prov.Person)
        self.assertEqual(dataset1.creator.name, 'John Doe')
        self.assertEqual(dataset1.version, '1.0')
        self.assertEqual(str(dataset1.identifier), 'http://example.com/dataset')
        self.assertIsInstance(dataset1.distribution[0], dcat.Distribution)
        self.assertEqual(dataset1.distribution[0].id, '_:b4')
        self.assertEqual(dataset1.distribution[0].title, 'Distribution title')
        self.assertEqual(dataset1.distribution[0].description, 'Distribution description')
        self.assertIsInstance(dataset1.distribution[0].creator, prov.Person)
        self.assertEqual(dataset1.distribution[0].creator.name, 'John Doe')
        self.assertEqual(dataset1.distribution[0].version, '1.0')
        self.assertEqual(str(dataset1.distribution[0].identifier), 'http://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].access_URL), 'http://example.com/distribution')
        self.assertEqual(str(dataset1.distribution[0].download_URL), 'http://example.com/distribution/download')
