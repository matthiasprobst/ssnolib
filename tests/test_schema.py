import pathlib

import ssnolib
import utils
from ssnolib import prov, StandardNameTable

__this_dir__ = pathlib.Path(__file__).parent

from ssnolib.schema import Project, ResearchProject

CACHE_DIR = ssnolib.utils.get_cache_dir()


class TestSchema(utils.ClassTest):

    def test_project(self):
        snt_dist = ssnolib.dcat.Distribution(
            downloadURL="https://sandbox.zenodo.org/records/123202/files/Standard_Name_Table_for_the_Property_Descriptions_of_Centrifugal_Fans.jsonld",
            media_type="application/json+ld"
        )

        dataset = ssnolib.dcat.Dataset(
            identifier="https://sandbox.zenodo.org/uploads/123202",
            distribution=snt_dist
        )

        proj = Project(
            identifier='http://example.com/project',
            funder=prov.Organization(name='Funder'),
            usesStandardnameTable=dataset
        )

        self.assertEqual(str(proj.identifier), 'http://example.com/project')
        self.assertIsInstance(proj.funder, prov.Organization)
        self.assertEqual(proj.funder.name, 'Funder')
        self.assertEqual(proj.id, 'http://example.com/project')

    def test_research_project(self):
        snt = StandardNameTable(title="My SNT")
        proj = ResearchProject(
            identifier='http://example.com/research_project',
            funder=prov.Organization(name='Funder'),
            usesStandardnameTable=snt
        )
        self.assertEqual(proj.usesStandardnameTable.title, 'My SNT')
        self.assertEqual(proj.id, 'http://example.com/research_project')

