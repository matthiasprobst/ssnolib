import json
import pathlib
import platform
import shutil
import unittest

import h5rdmtoolbox as h5tbx
import pydantic
import requests.exceptions
import yaml
from ontolutils.namespacelib.m4i import M4I

import ssnolib
import ssnolib.standard_name_table
from ssnolib import StandardName, StandardNameTable, Transformation
from ssnolib.dcat import Distribution
from ssnolib.namespace import SSNO
from ssnolib.prov import Attribution
from ssnolib.qudt import parse_unit
from ssnolib.standard_name import ScalarStandardName, VectorStandardName
from ssnolib.utils import download_file

__this_dir__ = pathlib.Path(__file__).parent

CACHE_DIR = ssnolib.utils.get_cache_dir()

SNT_JSONLD = """{
  "@context": {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "prov": "http://www.w3.org/ns/prov#",
    "ssno": "https://matthiasprobst.github.io/ssno#"
  },
  "@type": "ssno:StandardNameTable",
  "dct:title": "OpenCeFaDB Fan Standard Name Table",
    "prov:qualifiedAttribution": [
        {
            "@type": "prov:Attribution",
            "prov:agent": {
                "@type": "prov:Person",
                "foaf:firstName": "Matthias",
                "foaf:lastName": "Probst",
                "m4i:orcidId": "https://orcid.org/0000-0001-8729-0482",
                "@id": "https://orcid.org/0000-0001-8729-0482"
            },
            "prov:hadRole": "http://w3id.org/nfdi4ing/metadata4ing#ContactPerson",
            "@id": "_:Nb2d044e3f4834c249070f5d48f2a2110"
        },
        {
            "@type": "prov:Attribution",
            "prov:agent": {
                "@type": "prov:Person",
                "foaf:mbox": "john@doe.com",
                "foaf:firstName": "John",
                "foaf:lastName": "Doe",
                "schema:affiliation": {
                    "@type": "prov:Organization",
                    "foaf:name": "Awesome Institute",
                    "@id": "_:N9635d7b0338947ebb87c22da2acfc4c5"
                },
                "@id": "_:N74403c73be1c4cd4a724d8dbe8c37c1c"
            },
            "prov:hadRole": "http://w3id.org/nfdi4ing/metadata4ing#Supervisor",
            "@id": "_:Nac1247a4798b4830b19a82feef83bc1b"
        }
    ],
  "ssno:standardNames": [
    {
      "@type": "ssno:StandardName",
      "ssno:standardName": "absolute_pressure",
      "ssno:description": "Pressure is force per unit area. Absolute air pressure is pressure deviation to a total vacuum.",
      "ssni:unit": "Pa",
      "@id": "local:39257b94-d31c-480e-a43c-8ae7f57fae6d"
    },
    {
      "@type": "ssno:StandardName",
      "ssno:standardName": "ambient_static_pressure",
      "ssno:description": "Static air pressure is the amount of pressure exerted by air that is not moving. Ambient static air pressure is the static air pressure of the surrounding air.",
      "ssni:unit": "Pa",
      "@id": "local:0637ec26-310b-4b0a-bf4c-e51d4afccc7d"
    },
    {
      "@type": "ssno:StandardName",
      "ssno:standardName": "ambient_temperature",
      "ssno:description": "Air temperature is the bulk temperature of the air, not the surface (skin) temperature. Ambient air temperature is the temperature of the surrounding air.",
      "ssni:unit": "K",
      "@id": "local:3286d041-a826-4776-9d25-065dae107b55"
    },
    {
      "@type": "ssno:StandardName",
      "ssno:standardName": "auxiliary_fan_rotational_speed",
      "ssno:description": "Number of revolutions of an auxiliary fan.",
      "ssni:unit": "1/s",
      "@id": "local:2a521e9d-4481-4965-9b42-390db2da4c83"
    }
  ]
}"""


class TestSSNOStandardNameTable(unittest.TestCase):

    def tearDown(self):
        pathlib.Path('snt.json').unlink(missing_ok=True)
        pathlib.Path('snt.yaml').unlink(missing_ok=True)
        pathlib.Path('snt2.yaml').unlink(missing_ok=True)
        pathlib.Path('snt_with_mod.yaml').unlink(missing_ok=True)
        if pathlib.Path(__this_dir__ / 'tmp').exists():
            shutil.rmtree(pathlib.Path(__this_dir__ / 'tmp'))

    def test_multiple_agents(self):
        agent1 = ssnolib.Person(
            firstName="Matthias", lastName="Probst",
            orcidId="https://orcid.org/0000-0001-8729-0482",
            id="https://orcid.org/0000-0001-8729-0482")
        agent2 = ssnolib.Person(
            firstName="John", lastName="Doe")
        snt = ssnolib.StandardNameTable(
            title='SNT from scratch',
            version='v1',
            qualifiedAttribution=[
                Attribution(agent=agent1, hadRole=M4I.ContactPerson),
                Attribution(agent=agent2, hadRole=M4I.Supervisor)
            ]
        )
        self.assertEqual(
            "Matthias",
            snt.qualifiedAttribution[0].agent.firstName
        )
        self.assertEqual(
            "John",
            snt.qualifiedAttribution[1].agent.firstName
        )
        self.assertEqual(
            str(M4I.ContactPerson),
            str(snt.qualifiedAttribution[0].hadRole)
        )
        self.assertEqual(
            str(M4I.Supervisor),
            str(snt.qualifiedAttribution[1].hadRole)
        )

    def test_from_jsonld_file(self):
        snt = StandardNameTable.from_jsonld(__this_dir__ / 'data/simpleSNT.jsonld', limit=1)
        qualifications = [q for q in snt.hasModifier if isinstance(q, ssnolib.Qualification)]
        self.assertEqual(1, len(qualifications))
        print(snt.qualifiedAttribution)

    def test_standard_name_table(self):
        sn1 = StandardName(standard_name='x_velocity',
                           description='x component of velocity',
                           unit='m s-1')
        sn2 = StandardName(standard_name='y_velocity',
                           description='y component of velocity',
                           unit='m s-1')

        snt = StandardNameTable()
        self.assertEqual(0, len(snt.standardNames))
        snt.add_new_standard_name(
            StandardName(standard_name='z_velocity', description='z component of velocity', unit='m s-1')
        )
        self.assertEqual(1, len(snt.standardNames))

        snt = StandardNameTable(standardNames=[sn1, sn2])
        with open('snt.json', 'w') as f:
            f.write(snt.model_dump_jsonld())

        snt_loaded = list(StandardNameTable.from_jsonld(data=snt.model_dump_jsonld(), limit=None))
        self.assertEqual(len(snt_loaded), 1)
        self.assertEqual(len(snt_loaded[0].standardNames), 2)
        self.assertEqual(snt_loaded[0].standardNames[0].standardName, 'x_velocity')
        self.assertEqual(snt_loaded[0].standardNames[0].description, 'x component of velocity')
        self.assertEqual(snt_loaded[0].standardNames[0].unit, str(parse_unit('m s-1')))
        self.assertEqual(snt_loaded[0].standardNames[1].standardName, 'y_velocity')
        self.assertEqual(snt_loaded[0].standardNames[1].description, 'y component of velocity')
        self.assertEqual(snt_loaded[0].standardNames[1].unit, str(parse_unit('m s-1')))

        snt_loaded = StandardNameTable.from_jsonld(data=snt.model_dump_jsonld(), limit=1)
        self.assertEqual(len(snt_loaded.standardNames), 2)
        self.assertEqual(snt_loaded.standardNames[0].standardName, 'x_velocity')
        self.assertEqual(snt_loaded.standardNames[0].description, 'x component of velocity')
        self.assertEqual(snt_loaded.standardNames[0].unit, str(parse_unit('m s-1')))
        self.assertEqual(snt_loaded.standardNames[1].standardName, 'y_velocity')
        self.assertEqual(snt_loaded.standardNames[1].description, 'y component of velocity')
        self.assertEqual(snt_loaded.standardNames[1].unit, str(parse_unit('m s-1')))
        pathlib.Path('snt.json').unlink(missing_ok=True)

    def test_standard_name_from_jsonld(self):
        sn_jsonld = """{"@id": "local:39257b94-d31c-480e-a43c-8ae7f57fae6d",
   "@type": "https://matthiasprobst.github.io/ssno#StandardName",
   "https://matthiasprobst.github.io/ssno#standardName": "absolute_pressure",
   "https://matthiasprobst.github.io/ssno#unit": "Pa",
   "https://matthiasprobst.github.io/ssno#description": "Pressure is force per unit area. Absolute air pressure is pressure deviation to a total vacuum."}"""
        sn = StandardName.from_jsonld(data=json.loads(sn_jsonld))

    def test_standard_name_table_from_large_jsonld(self):
        snt = ssnolib.parse_table(__this_dir__ / "data/cf.jsonld", fmt='jsonld')
        self.assertEqual("cf-standard-name-table", snt.title)
        self.assertEqual("86", snt.version)

    def test_standard_name_alternative_parsing(self):
        snt = ssnolib.parse_table(__this_dir__ / "data/simpleSNT.jsonld", fmt='jsonld')
        self.assertEqual("SNT from scratch", snt.title)
        self.assertEqual("v1", snt.version)
        self.assertEqual(2, len(snt.hasModifier))
        self.assertEqual(3, len(snt.standardNames))
        qualifications = [q for q in snt.hasModifier if isinstance(q, ssnolib.VectorQualification)]
        self.assertEqual(1, len(qualifications))
        self.assertEqual("component", qualifications[0].name)
        self.assertEqual("The component of a vector", qualifications[0].description)
        self.assertEqual(3, len(qualifications[0].hasValidValues))

    def test_standard_name_table_from_jsonld(self):
        snt_jsonld_filename = pathlib.Path(__this_dir__, 'snt.json')
        with open(snt_jsonld_filename, 'w') as f:
            json.dump(json.loads(SNT_JSONLD), f)
        snt = StandardNameTable.parse(snt_jsonld_filename, fmt='jsonld')

        snt_jsonld_filename.unlink(missing_ok=True)
        self.assertEqual(snt.title, 'OpenCeFaDB Fan Standard Name Table')
        self.assertEqual(4, len(snt.standardNames))
        self.assertEqual(snt.standardNames[0].standardName, 'absolute_pressure')
        self.assertEqual(snt.standardNames[0].standard_name, 'absolute_pressure')
        self.assertEqual(snt.standardNames[0].description,
                         'Pressure is force per unit area. Absolute air pressure is pressure deviation to a total vacuum.')
        self.assertEqual(snt.standardNames[0].unit, 'http://qudt.org/vocab/unit/PA')
        self.assertEqual(snt.standardNames[1].standardName, 'ambient_static_pressure')
        self.assertEqual(snt.standardNames[1].standard_name, 'ambient_static_pressure')
        self.assertEqual(snt.standardNames[2].standardName, 'ambient_temperature')
        self.assertEqual(snt.standardNames[2].unit, 'http://qudt.org/vocab/unit/K')

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
                         'standardNames': {'x_velocity': {'description': 'x component of velocity',
                                                          'unit': 'm s-1'},
                                           'y_velocity': {'description': 'y component of velocity',
                                                          'unit': 'm s-1'}}}
        with open('snt.yaml', 'w') as f:
            yaml.dump(snt_yaml_data, f)
        snt = StandardNameTable.parse('snt.yaml', fmt='yaml')
        self.assertEqual(snt.title, 'SNT')

        snt = StandardNameTable.parse('snt.yaml', fmt=None)
        self.assertEqual(snt.title, 'SNT')

    def test_standard_name_table_from_xml(self):
        cf_contention = 'http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml'
        snt_xml_filename = download_file(cf_contention,
                                         dest_filename='snt.xml',
                                         exist_ok=True)
        self.assertTrue(snt_xml_filename.exists())

        xml_snt = StandardNameTable.parse(snt_xml_filename, fmt=None, make_standard_names_lowercase=True)
        self.assertEqual(
            xml_snt.qualifiedAttribution.agent.mbox,
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

        snt = StandardNameTable.parse(snt_xml_filename, fmt='xml', make_standard_names_lowercase=True)
        self.assertEqual(
            snt.qualifiedAttribution.agent.mbox,
            'support@ceda.ac.uk')
        snt_xml_filename.unlink(missing_ok=True)

        dist = Distribution(
            downloadURL='http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
            mediaType='application/xml')

        snt = StandardNameTable.parse(dist, make_standard_names_lowercase=True)
        self.assertEqual(
            snt.qualifiedAttribution.agent.mbox,
            'support@ceda.ac.uk'
        )
        self.assertEqual(snt.title, 'cf-standard-name-table')
        pathlib.Path(f'{snt.title}.xml').unlink(missing_ok=True)

        self.assertFalse(snt.verify_name("x_velocity"))

    def test_standard_name_table_to_yaml(self):
        snt_yaml_filename = pathlib.Path('snt.yaml')
        if not snt_yaml_filename.exists():
            self.test_standard_name_table_from_yaml()
        assert snt_yaml_filename.exists()
        snt = StandardNameTable.parse(snt_yaml_filename, fmt='yaml')
        snt.to_yaml('snt2.yaml', overwrite=True)

        with open('snt.yaml') as f:
            yaml1 = yaml.safe_load(f)
            for k, v in yaml1.copy()['standardNames'].items():
                yaml1['standardNames'][k]['unit'] = str(parse_unit(v['unit']))

        with open('snt2.yaml') as f:
            yaml2 = yaml.safe_load(f)

        self.assertDictEqual(yaml1, yaml2)

    def test_scalar_qualifications(self):
        medium = ssnolib.Qualification(name="medium", description="medium of a quantity",
                                       hasValidValues=["air", "water"],
                                       before=ssnolib.SSNO.AnyStandardName)
        snt = ssnolib.StandardNameTable(
            standard_names=[ssnolib.ScalarStandardName(standard_name="density", description="", unit="kg/m^3")])
        snt.hasModifier = [medium, ]
        self.assertTrue(snt.verify_name("density"))
        self.assertTrue(snt.verify_name("air_density"))

    def test_modifications(self):
        comp = ssnolib.Qualification(name="component",
                                     description="component of the vector",
                                     hasValidValues=['x', 'y', "z"])
        medium = ssnolib.Qualification(name="medium", description="medium", hasPreposition='in')
        medium.after = SSNO.AnyStandardName
        comp.before = SSNO.AnyStandardName

        snt = StandardNameTable(title='SNT with modifications')
        snt.hasModifier = [comp, medium]
        self.assertEqual("[component] standard_name [in medium]", snt.get_qualification_rule_as_string())

        snt.to_yaml('snt_with_mod.yaml', overwrite=True)

        new_snt = StandardNameTable.parse('snt_with_mod.yaml', fmt='yaml')
        self.assertEqual(new_snt.title, 'SNT with modifications')
        self.assertEqual("[component] standard_name [in medium]", new_snt.get_qualification_rule_as_string())

        # circular reference:
        medium.before = comp
        comp.after = medium
        with self.assertRaises(ValueError):
            medium.model_dump_jsonld()

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
            name="condition",
            description='A phrase assuming_condition indicates that the named quantity is the value which would obtain if all aspects of the system were unaltered except for the assumption of the circumstances specified by the condition. Possibilities are assuming_clear_sky, assuming_deep_snow, assuming_no_snow.',
            hasPreposition='assuming',
            hasValidValues=["clear_sky", "deep_snow", "no_snow"]
        )
        self.assertEqual([v.qualificationValue for v in condition.hasValidValues], ["clear_sky", "deep_snow", "no_snow"])

        # order the qualifications:
        from ssnolib.namespace import SSNO
        surface.before = component
        component.before = SSNO.AnyStandardName
        at_surface.after = SSNO.AnyStandardName
        medium.after = at_surface
        process.after = medium
        condition.after = process

        snt = StandardNameTable(
            title='CF Rebuilt'
        )
        snt.hasModifier = [surface, component, at_surface]

        self.assertEqual(
            "[surface] [component] standard_name [at surface]",
            snt.get_qualification_rule_as_string()
        )

        # snt = StandardNameTable(name='CF Rebuilt')
        snt.hasModifier = [surface, component, at_surface, medium, process, condition]

        self.assertEqual(
            "[surface] [component] standard_name [at surface] [in medium] [due to process] [assuming condition]",
            snt.get_qualification_rule_as_string()
        )

        core_scalar_standard_names = [
            ("air_density", "kg m-3"),
            ("air_pressure", "Pa"),
            ("temperature", "K"),
        ]
        core_vector_standard_names = [
            ("coordinate", "m"),
            ("velocity", "m/s"),
        ]
        with self.assertRaises(pydantic.ValidationError):
            snt.append("standardNames", 1.5)

        # snt.standardNames = StandardName(standardName="density", description="density", unit="kg/m-3")
        for csn in core_scalar_standard_names:
            snt.append("standardNames", ScalarStandardName(standardName=csn[0], description="", unit=csn[1]))
        for csn in core_vector_standard_names:
            snt.append("standardNames", VectorStandardName(standardName=csn[0], description="", unit=csn[1]))

        self.assertTrue(
            snt.verify_name("x_air_density")
        )  # density is not a vector standard name, hence x_ cannot be applied!
        self.assertTrue(
            snt.verify_name("x_coordinate")
        )
        self.assertTrue(
            snt.verify_name("tropopause_coordinate")
        )
        self.assertTrue(snt.verify_name("air_density"))  # equals "air_density"
        self.assertTrue(snt.verify_name("tropopause_air_pressure"))  # using regex
        tropopause_air_pressure = snt.get_standard_name("tropopause_air_pressure")  # using regex

        self.assertEqual(
            tropopause_air_pressure.description,
            snt.get_standard_name("air_pressure").description + surface.description)
        # TODO: Qualification -> validValues could be a list of
        #  QualificationValues(value='tropopause', description='The tropopause is the boundary between the troposphere and the stratosphere.'))
        #  this helps with these "means" statements: The surface called "surface" means the lower boundary of the atmosphere. sea_level means mean sea level, which is close to the geoid in sea areas
        #  This allows to build the cf-convention guidelines kind of...
        snt.add_new_standard_name(
            StandardName(
                standardName="tropopause_air_pressure",
                description="",
                unit="Pa"
            )
        )

    def test_cf_qualifications2(self):
        snt = StandardNameTable()
        surface = ssnolib.Qualification(
            name="surface",
            description="My surface",
            hasValidValues=["toa", "tropopause", "surface"]
        )
        component = ssnolib.VectorQualification(
            name="component",
            description='My component',
            hasValidValues=["x", "y"]
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
        component.before = surface
        surface.before = SSNO.AnyStandardName
        at_surface.after = SSNO.AnyStandardName
        snt.hasModifier = [surface, component, at_surface]

        self.assertFalse(snt.verify_name("x_velocity"))

        snt.add_new_standard_name(VectorStandardName(standard_name='velocity', unit='m/s', description='velocity'),
                                  False)
        snt.add_new_standard_name(ScalarStandardName(standard_name='pressure', unit='Pa', description='pressure'),
                                  False)
        # self.assertTrue(snt.verify_name("x_velocity"))
        # self.assertTrue(snt.verify_name("toa_velocity"))
        # self.assertFalse(snt.verify_name("invalid_velocity"))
        self.assertTrue(snt.verify_name("x_toa_velocity_at_sea_floor"))
        self.assertFalse(
            snt.verify_name("x_toa_pressure_at_sea_floor"))  # component is not applicable to pressure (scalar)
        # self.assertTrue(snt.verify_name("x_toa_pressure"))
        # self.assertFalse(snt.verify_name("toa_x_velocity"))

    if platform.system() != "Darwin":  # pandoc could not be installed in CI for macos... to be solved...
        def test_to_html(self):
            cf_contention = 'http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml'
            snt_xml_filename = download_file(cf_contention,
                                             dest_filename='snt.xml',
                                             exist_ok=True)
            self.assertTrue(snt_xml_filename.exists())

            xml_snt = StandardNameTable.parse(snt_xml_filename, fmt=None, make_standard_names_lowercase=True)
            xml_snt.description = f"This table is built by from {snt_xml_filename}. This is not complete, but an excerpt!"

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
                name="condition",
                description='A phrase assuming_condition indicates that the named quantity is the value which would obtain if all aspects of the system were unaltered except for the assumption of the circumstances specified by the condition. Possibilities are assuming_clear_sky, assuming_deep_snow, assuming_no_snow.',
                hasPreposition='assuming',
                hasValidValues=["clear_sky", "deep_snow", "no_snow"]
            )

            # order the qualifications:
            surface.before = component
            component.before = SSNO.AnyStandardName
            at_surface.after = SSNO.AnyStandardName
            medium.after = at_surface
            process.after = medium
            condition.after = process

            change_over_time = Transformation(
                name="change_over_time_in_X",
                description="change in a quantity X over a time-interval, which should be defined by the bounds of the time coordinate.",
                altersUnit="[X]",
                hasCharacter=[ssnolib.Character(character="X", associatedWith=SSNO.AnyStandardName)]
            )
            component_derivative_of_X = Transformation(
                name="C_derivative_of_X",
                description="derivative of X with respect to distance in the component direction, which may be northward, "
                            "southward, eastward, westward, x or y. The last two indicate derivatives along the axes of "
                            "the grid, in the case where they are not true longitude and latitude.",
                altersUnit="[X]/[C]",
                hasCharacter=[ssnolib.Character(character="C", associatedWith=component),
                              ssnolib.Character(character="X", associatedWith=SSNO.AnyStandardName)]
            )
            xml_snt.hasModifier = [
                surface,
                component,
                at_surface,
                medium,
                process,
                condition,
                change_over_time,
                component_derivative_of_X
            ]

            with self.assertRaises(ValueError):
                _ = xml_snt.to_html(folder="tmp", filename="snt.html")

            filename = xml_snt.to_html()
            self.assertTrue(filename.exists())
            self.assertEqual(filename.name, f"{xml_snt.title}.html")
            filename.unlink(missing_ok=True)
            snt_xml_filename.unlink(missing_ok=True)

            # save using a custom file:
            filename = xml_snt.to_html(filename='snt.html')
            self.assertTrue(filename.exists())
            self.assertEqual(filename.name, "snt.html")
            filename.unlink(missing_ok=True)
            snt_xml_filename.unlink(missing_ok=True)

            # save to folder:
            folder = __this_dir__ / 'tmp'
            folder.mkdir(exist_ok=True, parents=True)
            filename = xml_snt.to_html(folder=folder)
            self.assertTrue(filename.exists())
            self.assertEqual(filename.parent.name, "tmp")
            self.assertEqual(filename.name, f"{xml_snt.title}.html")
            filename.unlink(missing_ok=True)
            snt_xml_filename.unlink(missing_ok=True)

    def test_regex(self):
        a = ssnolib.Qualification(
            name="a",
            description='a',
            hasValidValues=["a", "aa", "aaa"]
        )
        b = ssnolib.Qualification(
            name="b",
            description='b',
            hasValidValues=["b", "bb", "bbb"]
        )
        c = ssnolib.Qualification(
            name="c",
            description='c',
            hasValidValues=["c", "cc", "ccc"]
        )
        d = ssnolib.Qualification(
            name="d",
            description='d',
            hasValidValues=["d", "dd", "ddd"]
        )

        # order the qualifications:
        from ssnolib.namespace import SSNO
        a.before = b
        b.before = SSNO.AnyStandardName
        c.after = SSNO.AnyStandardName
        d.after = c

        snt = StandardNameTable(name='CF Rebuilt')
        snt.hasModifier = [a, b, c, d]

        core_standard_names = [
            ("density", "kg m-3", "Density of a fluid or gas."),
            ("pressure", "Pa"),
            ("temperature", "K"),
            ("speed", "m/s")
        ]

        # snt.standardNames = StandardName(standardName="density", description="density", unit="kg/m-3")
        for csn in core_standard_names:
            snt.append("standardNames", StandardName(standardName=csn[0], description="", unit=csn[1]))

        self.assertEqual(
            r"^(?:(a|aa|aaa))?_?(?:(b|bb|bbb))?_?standard_name_?(?:(c|cc|ccc))?_?(?:(d|dd|ddd))?$",
            snt.get_qualification_regex()[0]
        )
        self.assertTrue(snt.verify_name("density"))  # equals "air_density"
        self.assertTrue(snt.verify_name("a_density"))  # using regex
        self.assertTrue(snt.verify_name("aa_density"))  # using regex
        self.assertTrue(snt.verify_name("aaa_density"))  # using regex
        self.assertTrue(snt.verify_name("a_density_c"))  # using regex
        self.assertTrue(snt.verify_name("a_density_d"))  # using regex
        self.assertTrue(snt.verify_name("a_density_c_d"))  # using regex
        self.assertTrue(snt.verify_name("a_b_density_c"))  # using regex
        self.assertTrue(snt.verify_name("a_b_density_c_d"))  # using regex

    def test_transformation(self):
        # taken from https://cfconventions.org/Data/cf-standard-names/docs/guidelines.html#process
        X = ssnolib.Character(character="X", associatedWith=ssnolib.namespace.SSNO.AnyStandardName)
        Y = ssnolib.Character(character="Y", associatedWith=ssnolib.namespace.SSNO.AnyStandardName)
        t = ssnolib.Transformation(
            name="derivative_of_X_wrt_Y",
            altersUnit="[X]/[Y]",
            hasCharacter=[X, Y],
            description="dX/dY (keeping any other independent variables constant, i.e. the partial derivative if appropriate).")
        snt = StandardNameTable(name='CF Rebuilt')
        snt.hasModifier = [t]
        self.assertEqual(t.altersUnit, "[X]/[Y]")
        self.assertEqual(
            t.description,
            "dX/dY (keeping any other independent variables constant, i.e. the partial derivative if appropriate).")
        self.assertEqual(t.name, "derivative_of_X_wrt_Y")
        self.assertEqual(t.name, snt.hasModifier[0].name)

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
