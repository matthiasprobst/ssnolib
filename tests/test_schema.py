import pathlib

from ontolutils.ex import prov

import ssnolib
import utils
from ssnolib import StandardNameTable
from ssnolib.schema import Project, ResearchProject
from ontolutils.ex import dcat

__this_dir__ = pathlib.Path(__file__).parent

CACHE_DIR = ssnolib.utils.get_cache_dir()


class TestSchema(utils.ClassTest):

    def test_project(self):
        snt_dist = dcat.Distribution(
            downloadURL="https://sandbox.zenodo.org/records/123202/files/Standard_Name_Table_for_the_Property_Descriptions_of_Centrifugal_Fans.jsonld",
            media_type="application/json+ld"
        )

        dataset = dcat.Dataset(
            identifier="https://sandbox.zenodo.org/uploads/123202",
            distribution=snt_dist
        )

        proj = Project(
            identifier='https://example.com/project',
            funder=prov.Organization(name='Funder'),
            usesStandardnameTable=dataset
        )

        self.assertEqual(str(proj.identifier), 'https://example.com/project')
        self.assertIsInstance(proj.funder, prov.Organization)
        self.assertEqual(proj.funder.name, 'Funder')
        self.assertEqual(proj.id, 'https://example.com/project')

    def test_research_project(self):
        snt = StandardNameTable(title="My SNT")
        proj = ResearchProject(
            identifier='https://example.com/research_project',
            funder=prov.Organization(name='Funder'),
            usesStandardnameTable=snt
        )
        self.assertEqual(proj.usesStandardnameTable.title, 'My SNT')
        self.assertEqual(proj.id, 'https://example.com/research_project')

        print(proj.serialize("ttl"))
