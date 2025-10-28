import unittest

import pydantic

from ssnolib import StandardName
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

        ds2 = Dataset(name='/Group1/Dataset2', standard_name="x_velocity")
        self.assertEqual(ds2.name, '/Group1/Dataset2')
        self.assertEqual(ds2.standard_name, "x_velocity")
        self.assertEqual(ds2.serialize("ttl"), """@prefix hdf5: <http://purl.allotrope.org/ontologies/hdf5/1.8#> .
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

[] a hdf5:Dataset ;
    hdf5:name "/Group1/Dataset2" ;
    ssno:standardName "x_velocity" .

""")

        with self.assertRaises(pydantic.ValidationError):
            Dataset(name='/Group1/Dataset3', has_standard_name="x_velocity")

        ds3 = Dataset(name='/Group1/Dataset3',
                      has_standard_name=StandardName(standard_name="y_velocity",
                                                     unit="http://qudt.org/vocab/unit/M-PER-SEC")
                      )
        self.assertEqual(ds3.name, '/Group1/Dataset3')
        self.assertEqual(ds3.has_standard_name.standard_name, "y_velocity")
        self.assertEqual(ds3.has_standard_name.unit, "http://qudt.org/vocab/unit/M-PER-SEC")
        self.assertEqual(ds3.serialize("ttl"), """@prefix hdf5: <http://purl.allotrope.org/ontologies/hdf5/1.8#> .
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

[] a hdf5:Dataset ;
    hdf5:name "/Group1/Dataset3" ;
    ssno:hasStandardName [ a ssno:StandardName ;
            ssno:standardName "y_velocity" ;
            ssno:unit <http://qudt.org/vocab/unit/M-PER-SEC> ] .

""")

        sn = StandardName(id="https://doi.org/123/sn1",
                          standard_name="z_velocity",
                          unit="http://qudt.org/vocab/unit/M-PER-SEC")
        ds4 = Dataset(name='/Group1/Dataset4', has_standard_name=sn.id)
        self.assertEqual(ds4.name, '/Group1/Dataset4')
        self.assertEqual(ds4.has_standard_name, sn.id)
        self.assertEqual(ds4.serialize("ttl"), """@prefix hdf5: <http://purl.allotrope.org/ontologies/hdf5/1.8#> .
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

[] a hdf5:Dataset ;
    hdf5:name "/Group1/Dataset4" ;
    ssno:hasStandardName <https://doi.org/123/sn1> .

""")

    def testGroup(self):
        with self.assertRaises(pydantic.ValidationError):
            Group(name='Group1')
        grp1 = Group(name='/Group1')
        self.assertEqual(grp1.serialize("ttl"), """@prefix hdf5: <http://purl.allotrope.org/ontologies/hdf5/1.8#> .

[] a hdf5:Group ;
    hdf5:name "/Group1" .

""")
