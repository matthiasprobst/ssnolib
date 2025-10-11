import ast
import importlib
import pathlib
import sys
import unittest

from ontolutils import get_urirefs

import ssnolib
from ssnolib import SSNO

__this_dir__ = pathlib.Path(__file__).parent


class TestSSNO(unittest.TestCase):

    def test_python_classes(self):
        namespace_names = [str(n).split('#', 1)[-1] for n in list(SSNO.__dict__.values())]
        ssnolib_module_folder = __this_dir__ / "../ssnolib/ssno"

        sys.path.insert(0, str(ssnolib_module_folder.resolve().parent))
        module = importlib.import_module("ssno")
        ignore = ["AgentRole"]
        ignore_filenames = ["__init__.py", "plugins.py", "parser.py"]
        self.assertTrue(ssnolib_module_folder.exists())
        for filename in ssnolib_module_folder.glob("*.py"):
            if filename.name not in ignore_filenames:
                with open(filename, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read(), filename=filename)
                classes = [n.name for n in ast.walk(node) if isinstance(n, ast.ClassDef)]
                for cls_name in classes:
                    if cls_name not in ignore:
                        cls = getattr(module, cls_name)
                        for iri in get_urirefs(cls).values():
                            if "ssno:" in iri:
                                self.assertIn(iri.split(":", 1)[-1], namespace_names)
                        self.assertTrue(cls_name in namespace_names, f"Class {cls_name} in {filename} not in namespace")

    def test_readme_example(self):

        air_temp = ssnolib.StandardName(
            standardName='air_temperature',
            unit='K',
            description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.@en')
        ttl = air_temp.model_dump_ttl()
        self.assertEqual(ttl, """@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

[] a ssno:StandardName ;
    ssno:description "Air temperature is the bulk temperature of the air, not the surface (skin) temperature."@en ;
    ssno:standardName "air_temperature" ;
    ssno:unit <http://qudt.org/vocab/unit/K> .

""")