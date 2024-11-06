import unittest

import pydantic

from ssnolib.hdf5 import File, Dataset, Group


class TestHDF5(unittest.TestCase):

    def testHDF5File(self):
        root_group = Group(name="/")
        self.assertEqual(root_group.name, "/")
        file = File(rootGroup=root_group)
        self.assertEqual(file.rootGroup.name, "/")

        group = Group(name="/grp")
        with self.assertRaises(pydantic.ValidationError):
            File(rootGroup=group)

    def testDataset(self):
        with self.assertRaises(pydantic.ValidationError):
            Dataset(name='Dataset1')
        ds1 = Dataset(name='/Dataset1')
        self.assertEqual(ds1.name, '/Dataset1')

    def testGroup(self):
        with self.assertRaises(pydantic.ValidationError):
            Group(name='Group1')
        grp1 = Group(name='/Group1')
