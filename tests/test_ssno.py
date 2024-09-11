import json
import pathlib
import unittest

import h5rdmtoolbox as h5tbx
import ontolutils
import requests.exceptions
import yaml
from ontolutils import QUDT_UNIT

import ssnolib
import ssnolib.standard_name_table
from ssnolib import StandardName, StandardNameTable
from ssnolib.dcat import Distribution
from ssnolib.namespace import SSNO
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

    def test_standard_name_table_to_yaml(self):
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

    def test_modifications(self):
        comp = ssnolib.Qualification(name="component", description="component of the vector")
        medium = ssnolib.Qualification(name="medium", description="medium")
        medium.before = comp
        comp.after = medium
        with self.assertRaises(ValueError):
            medium.model_dump_jsonld()

        comp.after = SSNO.AnyStandardName
        print(medium.model_dump_jsonld())

    def test_cf_qualifications(self):
        # Taken from https://cfconventions.org/Data/cf-standard-names/docs/guidelines.html#id2797725
        surface = ssnolib.Qualification(
            name="surface",
            description='A surface is defined as a function of horizontal position. Surfaces which are defined using a coordinate value (e.g. height of 1.5 m) are indicated by a single-valued coordinate variable, not by the standard name. In the standard name, some surfaces are named by single words which are placed at the start: toa (top of atmosphere), tropopause, surface. Other surfaces are named by multi-word phrases put after at: at_adiabatic_condensation_level, at_cloud_top, at_convective_cloud_top, at_cloud_base, at_convective_cloud_base, at_freezing_level, at_ground_level, at_maximum_wind_speed_level, at_sea_floor, at_sea_ice_base, at_sea_level, at_top_of_atmosphere_boundary_layer, at_top_of_atmosphere_model, at_top_of_dry_convection. The surface called "surface" means the lower boundary of the atmosphere. sea_level means mean sea level, which is close to the geoid in sea areas. ground_level means the land surface (beneath the snow and surface water, if any). cloud_base refers to the base of the lowest cloud. cloud_top refers to the top of the highest cloud. Fluxes at the top_of_atmosphere_model differ from TOA fluxes only if the model TOA fluxes make some allowance for the atmosphere above the top of the model; if not, it is usual to give standard names with toa to the fluxes at the top of the model atmosphere.',
            hasValidValues=["toa", "tropopause", "surface"]
        )
        component = ssnolib.Qualification(
            name="component",
            description='The direction of the spatial component of a vector is indicated by one of the words upward, downward, northward, southward, eastward, westward, x, y. The last two indicate directions along the horizontal grid being used when they are not true longitude and latitude (if there is a rotated pole, for instance). If the standard name indicates a tensor quantity, two of these direction words may be included, applying to two of the spatial dimensions Z Y X, in that order. If only one component is indicated for a tensor, it means the flux in the indicated direction of the magnitude of the vector quantity in the plane of the other two spatial dimensions. The names of vertical components of radiative fluxes are prefixed with net_, thus: net_downward and net_upward. This treatment is not applied for any kinds of flux other than radiative. Radiative fluxes from above and below are often measured and calculated separately, the "net" being the difference. Within the atmosphere, radiation from below (not net) is indicated by a prefix of upwelling, and from above with downwelling. For the top of the atmosphere, the prefixes incoming and outgoing are used instead.,',
            hasValidValues=["upward", "downward", "northward", "southward", "eastward", "westward", "x", "y"]
        )
        at_surface = ssnolib.Qualification(
            name="surface",
            description=surface.description,
            hasPreposition='at',
            hasValidValues=["adiabatic_condensation_level", "cloud_top", "convective_cloud_top",
                            "cloud_base",
                            "convective_cloud_base", "freezing_level", "ground_level",
                            "maximum_wind_speed_level",
                            "sea_floor", "sea_ice_base", "sea_level", "top_of_atmosphere_boundary_layer",
                            "top_of_atmosphere_model", "top_of_dry_convection"]
        )
        medium = ssnolib.Qualification(
            name="medium",
            description='A medium indicates the local medium or layer within which an intensive quantity applies: in_air, in_atmosphere_boundary_layer, in_mesosphere, in_sea_ice, in_sea_water, in_soil, in_soil_water, in_stratosphere, in_thermosphere, in_troposphere.',
            hasPreposition='in',
            hasValidValues=['air', 'atmosphere_boundary_layer', "mesosphere", "sea_ice", "sea_water", "soil",
                            "soil_water", "stratosphere", "thermosphere", "troposphere"]
        )
        process = ssnolib.Qualification(
            name="process",
            description='The specification of a physical process by the phrase due_to_process means that the quantity named is a single term in a sum of terms which together compose the general quantity named by omitting the phrase. Possibilites are: due_to_advection, due_to_convection, due_to_deep_convection, due_to_diabatic_processes, due_to_diffusion, due_to_dry_convection, due_to_gravity_wave_drag, due_to_gyre, due_to_isostatic_adjustment, due_to_large_scale_precipitation, due_to_longwave_heating, due_to_moist_convection, due_to_overturning, due_to_shallow_convection, due_to_shortwave_heating, due_to_thermodynamics (referring to sea ice freezing and melting).',
            hasPreposition='due_to',
            hasValidValues=["advection", "convection", "deep_convection", "diabatic_processes",
                            "diffusion", "dry_convection", "gravity_wave_drag", "gyre", "isostatic_adjustment",
                            "large_scale_precipitation", "longwave_heating", "moist_convection", "overturning",
                            "shallow_convection", "shortwave_heating", "thermodynamics"]
        )
        condition = ssnolib.Qualification(
            name="process",
            description='A phrase assuming_condition indicates that the named quantity is the value which would obtain if all aspects of the system were unaltered except for the assumption of the circumstances specified by the condition. Possibilities are assuming_clear_sky, assuming_deep_snow, assuming_no_snow.',
            hasPreposition='assuming',
            hasValidValues=["clear_sky", "deep_snow", "no_snow"]
        )
        self.assertEqual(condition.hasValidValues, ["clear_sky", "deep_snow", "no_snow"])

        # order the qualifications:
        from ssnolib.namespace import SSNO
        surface.before = component
        component.before = SSNO.AnyStandardName
        at_surface.after = SSNO.AnyStandardName
        medium.after = at_surface
        process.after = medium
        condition.after = process

        snt = StandardNameTable(name='CF Rebuilt')
        snt.definesStandardNameModification = [surface, component, at_surface, medium, process, condition]

        self.assertEqual(
            "[surface] [component] standard_name [at_surface] [in_medium] [due_to_process] [assuming_process]",
            snt.get_qualification_rule_as_string())
        print(snt.get_qualification_rule_as_string())

    def test_transformation(self):
        # taken from https://cfconventions.org/Data/cf-standard-names/docs/guidelines.html#process
        t = ssnolib.Transformation(name="derivative_of_X_wrt_Y",
                               altersUnit="[X]/[Y]",
                               description="dX/dY (keeping any other independent variables constant, i.e. the partial derivative if appropriate).")
        snt = StandardNameTable(name = 'CF Rebuilt')
        snt.definesStandardNameModification = [t]
        self.assertEqual(t.altersUnit, "[X]/[Y]")
        self.assertEqual(t.description, "dX/dY (keeping any other independent variables constant, i.e. the partial derivative if appropriate).")
        self.assertEqual(t.name, "derivative_of_X_wrt_Y")
        self.assertEqual(t.name, snt.definesStandardNameModification[0].name)


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
