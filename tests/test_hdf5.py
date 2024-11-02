import unittest

import pydantic

from ssnolib.hdf5 import File, Dataset, Group, RootGroup


class TestHDF5(unittest.TestCase):

    def testHDF5File(self):
        root_group = RootGroup()
        self.assertEqual(root_group.name, "/")
        file = File(rootGroup=root_group)
        self.assertEqual(file.rootGroup.name, "/")

        group = Group()
        with self.assertRaises(pydantic.ValidationError):
            File(rootGroup=group)

    def testDataset(self):
        with self.assertRaises(pydantic.ValidationError):
            Dataset(name='Dataset1')
        ds1 = Dataset(name='/Dataset1')
        self.assertEqual(ds1.name, '/Dataset1')
        dataset = Dataset()

    def testGroup(self):
        with self.assertRaises(pydantic.ValidationError):
            Group(name='Group1')
        grp1 = Group(name='/Group1')

    def testRootGroup(self):
        grp1 = Group(name='/Group1')
        grp2 = Group(name='/Group2')
        ds1 = Group(name='/Dataset1')
        root_group1 = RootGroup(member=grp1)
        root_group2 = RootGroup(member=[grp1, grp2])
        root_group3 = RootGroup(member=[grp1, ds1])

        self.assertEqual(root_group1.member, grp1)
        self.assertEqual(root_group1.member.name, "/Group1")
        self.assertEqual(root_group2.member[0].name, "/Group1")
        self.assertEqual(root_group2.member[1].name, "/Group2")
        self.assertEqual(root_group3.member[0].name, "/Group1")
        self.assertEqual(root_group3.member[1].name, "/Dataset1")
