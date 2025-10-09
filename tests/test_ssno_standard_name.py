import pathlib
import unittest

import ontolutils
import pydantic
from ontolutils import QUDT_UNIT
from ontolutils.utils.qudt_units import parse_unit
from pydantic import ValidationError

import ssnolib
from ssnolib import StandardName, StandardNameTable
from ssnolib.prov import Person
from ssnolib.skos import Note

__this_dir__ = pathlib.Path(__file__).parent

CACHE_DIR = ssnolib.utils.get_cache_dir()


class TestSSNOStandardName(unittest.TestCase):

    def test_date_literal_for_note(self):
        note = Note(value="note", created="2025-01-04")
        print(note)
        print(note.model_dump_ttl())

    def test_standard_name_and_table(self):
        snt = StandardNameTable(title="my snt")
        sn = StandardName(
            standard_name='x_velocity',
            unit="m/s",
            description='x component of velocity',
            standardNameTable=snt
        )
        self.assertEqual(sn.standardNameTable.title, "my snt")

    def test_standard_name_alias(self):
        sn = StandardName(standard_name='x_velocity',
                          description='x component of velocity',
                          unit='m/s')
        sn_alias = StandardName(standardName='x_velocity',
                                description='x component of velocity',
                                unit='m/s',
                                alias=sn)
        self.assertEqual(sn.standard_name, 'x_velocity')
        self.assertEqual(sn.description, 'x component of velocity')
        self.assertEqual(sn.unit, sn_alias.unit)

        sn_alias = StandardName(standardName='x_velocity',
                                description='x component of velocity',
                                unit='m/s',
                                alias=sn.id)
        self.assertEqual(sn_alias.alias, sn.id)
        self.assertEqual(sn.standardName, sn_alias.standardName)
        self.assertEqual(sn.unit, sn_alias.unit)
        self.assertEqual(sn.description, sn_alias.description)

    def test_units(self):
        sn = StandardName(
            standard_name='x_velocity',
            description='x component of velocity',
            unit=''
        )
        self.assertEqual(sn.unit, str(QUDT_UNIT.UNITLESS))
        sn = StandardName(
            standard_name='x_velocity',
            description='x component of velocity',
            unit='1'
        )
        self.assertEqual(sn.unit, str(QUDT_UNIT.UNITLESS))

    def test_instantiating_standard_name_missing_fields(self):
        with self.assertRaises(pydantic.ValidationError):
            sn = StandardName()
        with self.assertRaises(pydantic.ValidationError):
            sn = StandardName(standardName='x_velocity', )
        with self.assertRaises(pydantic.ValidationError):
            sn = StandardName(standardName='x_velocity',
                              description='x component of velocity')

    def test_instantiating_standard_name(self):
        snt = StandardNameTable()
        sn = StandardName(standardName='x_velocity',
                          description='x component of velocity',
                          unit=QUDT_UNIT.M_PER_SEC,
                          standardNameTable=snt)
        self.assertIsInstance(sn, ontolutils.Thing)
        self.assertIsInstance(sn, StandardName)
        self.assertEqual(sn.standardName, 'x_velocity')
        self.assertEqual(sn.standard_name, 'x_velocity')
        self.assertEqual(sn.description, 'x component of velocity')
        self.assertEqual(sn.unit, str(parse_unit('m s-1')))
        self.assertEqual(sn.unit, str(parse_unit('m s-1')))
        self.assertIsInstance(sn.standard_name_table, StandardNameTable)
        self.assertEqual(snt.id, sn.standardNameTable.id)

        sn = StandardName(standardName='x_velocity',
                          description='x component of velocity',
                          unit=None)
        self.assertEqual(str(sn.unit), "http://qudt.org/vocab/unit/UNITLESS")

        with self.assertRaises(pydantic.ValidationError):
            StandardName(standardName='x_velocity',
                         description='x component of velocity',
                         unit="213nlsfh8os")

        try:
            StandardName(standardName='x_velocity',
                         description='x component of velocity',
                         unit="213nlsfh8os")
        except pydantic.ValidationError as e:
            self.assertEqual(e.errors()[0]['loc'], ('unit', 'unit'))
            self.assertEqual(e.errors()[0]['msg'],
                             'Value error, your_message Unable to parse: "213nlsfh8os" of standard name "x_velocity"')

        sn = StandardName(standardName='x_velocity',
                          description='x component of velocity',
                          unit=QUDT_UNIT.M_PER_SEC)
        self.assertEqual(str(sn.unit), 'http://qudt.org/vocab/unit/M-PER-SEC')

    def test_instantiating_standard_name_using_aliases(self):
        snt = StandardNameTable()
        sn = StandardName(standard_name='x_velocity',
                          description='x component of velocity',
                          unit=QUDT_UNIT.M_PER_SEC,
                          standard_name_table=snt)
        self.assertIsInstance(sn, ontolutils.Thing)
        self.assertIsInstance(sn, StandardName)
        self.assertEqual(sn.standardName, 'x_velocity')
        self.assertEqual(sn.standard_name, 'x_velocity')
        self.assertEqual(sn.description, 'x component of velocity')
        self.assertEqual(sn.unit, str(parse_unit('m s-1')))
        self.assertEqual(sn.unit, str(parse_unit('m s-1')))
        self.assertIsInstance(sn.standard_name_table, StandardNameTable)
        self.assertEqual(snt.id, sn.standard_name_table.id)

    def test_instantiating_standard_name_with_snt(self):
        sn = StandardName(standard_name='x_velocity',
                          unit=QUDT_UNIT.M_PER_SEC,
                          standard_name_table="https://doi.org/10.5281/zenodo.10428817")
        self.assertEqual(sn.standardNameTable, "https://doi.org/10.5281/zenodo.10428817")

        with self.assertRaises(pydantic.ValidationError):
            StandardName(standard_name='x_velocity',
                         unit=QUDT_UNIT.M_PER_SEC,
                         standard_name_table="123")

    def test_standard_name_jsonld(self):
        sn = StandardName(standard_name='x_velocity',
                          description='x component of velocity',
                          unit='m s-1')
        self.assertEqual(sn.unit, str(parse_unit('m s-1')))

        with open('sn.jsonld', 'w') as f:
            f.write(sn.model_dump_jsonld())

        sn_loaded = ontolutils.query(StandardName, source='sn.jsonld')
        self.assertEqual(len(sn_loaded), 1)
        self.assertEqual(sn_loaded[0].standardName, 'x_velocity')
        self.assertEqual(sn_loaded[0].description, 'x component of velocity')
        self.assertEqual(sn_loaded[0].unit, str(parse_unit('m s-1')))

        sn_loaded = StandardName.from_jsonld(data=sn.model_dump_jsonld())
        self.assertEqual(len(sn_loaded), 1)
        self.assertEqual(sn_loaded[0].standardName, 'x_velocity')
        self.assertEqual(sn_loaded[0].description, 'x component of velocity')
        self.assertEqual(sn_loaded[0].unit, str(parse_unit('m s-1')))

        pathlib.Path('sn.jsonld').unlink(missing_ok=True)

    def test_invalid_standard_names(self):
        # Wrong type for description:
        with self.assertRaises(pydantic.ValidationError):
            ssnolib.StandardName(
                standard_name='x_velocity',
                unit='m/s',
                description=123
            )

        # Incorrect standard name that does not match the basic pattern:
        with self.assertRaises(pydantic.ValidationError):
            ssnolib.StandardName(
                standard_name='X_velocity_',
                unit='m/s',
                description="invalid standard name"
            )

        # Cannot parse unit
        with self.assertRaises(ValidationError):
            ssnolib.StandardName(
                standard_name='x_velocity',
                unit='meterprosec',
                description="invalid standard name"
            )

        # Missing field(s)
        with self.assertRaises(pydantic.ValidationError):
            ssnolib.StandardName(
                standard_name='x_velocity',
                description="invalid standard name"
            )

    def test_standard_name_with_table(self):
        snt = StandardNameTable(identifier='https://doi.org/10.5281/zenodo.10428817')

        xvel = StandardName(
            standard_name="x_velocity",
            description="x component of velocity",
            unit="m/s",
            standardNameTable=snt
        )
        self.assertEqual(xvel.__str__(), 'x_velocity')
        self.assertEqual(xvel.standardNameTable, snt)

    def test_standard_name_with_difficult_unit(self):
        sn = StandardName(standardName="velocity", description="velocity", unit="m2/s2")
        self.assertEqual(str(sn.unit), 'http://qudt.org/vocab/unit/M2-PER-SEC2')

    def test_standard_name_table_with_note(self):
        snt_loaded = StandardNameTable.parse(__this_dir__ / f"data/snt_from_scratch.jsonld")
        snt_loaded.editorialNote = "This is an editorial note."
        self.assertEqual(snt_loaded.editorialNote, "This is an editorial note.")
        snt_loaded.editorialNote = Note(
            creator=Person(id="https://example.org/#creator"),
            value="This is an editorial note with a creator.@en"
        )
        self.assertIsInstance(snt_loaded.editorialNote, Note)
        self.assertEqual(snt_loaded.editorialNote.value, "This is an editorial note with a creator.")
        self.assertEqual(snt_loaded.editorialNote.creator.id, "https://example.org/#creator")
