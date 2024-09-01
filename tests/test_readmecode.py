import pathlib
import unittest



class TestReadme(unittest.TestCase):

    def tearDown(self):
        pathlib.Path('cf79.jsonld').unlink(missing_ok=True)
        pathlib.Path('air_temperature.jsonld').unlink(missing_ok=True)

    def test_code1(self):
        import ssnolib
        from ssnolib.dcat import Distribution

        distribution = Distribution(
            title='XML Table',
            download_URL='http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
            media_type='application/xml'
        )
        snt = ssnolib.StandardNameTable(title='CF Standard Name Table (latest version)',
                                        distribution=distribution)

        print(snt.model_dump_jsonld())

    def test_code2(self):
        import ssnolib
        from ssnolib.dcat import Distribution

        # Create a distribution object (downloadable XML file containing the standard name table)
        distribution = Distribution(title='XML Table',
                                    download_URL='http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
                                    media_type='application/xml')

        # Create a standard name table object
        snt = ssnolib.StandardNameTable(title='CF Standard Name Table v79',
                                        distribution=[distribution, ])

        # To describe this standard name table, we can export the JSON-LD file:
        with open('cf79.jsonld', 'w', encoding='utf-8') as f:
            f.write(snt.model_dump_jsonld())

    def test_code3(self):
        import ssnolib

        air_temp = ssnolib.StandardName(standard_name='air_temperature',
                                        canonical_units='K',
                                        description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')

        # write to JSON-LD
        with open('air_temperature.jsonld', 'w') as f:
            f.write(air_temp.model_dump_jsonld())