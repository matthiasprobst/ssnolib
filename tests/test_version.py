import json
import pathlib
import unittest

import ssnolib

__this_dir__ = pathlib.Path(__file__).parent


class TestVersion(unittest.TestCase):

    def test_version(self):
        this_version = 'x.x.x'
        setupcfg_filename = __this_dir__ / '../setup.cfg'
        with open(setupcfg_filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'version' in line:
                    this_version = line.split(' = ')[-1].strip()
        self.assertEqual(ssnolib.__version__, this_version)

    def test_codemeta(self):
        """checking if the version in codemeta.json is the same as the one of the toolbox"""

        with open(__this_dir__ / '../codemeta.json', 'r') as f:
            codemeta = json.loads(f.read())

        assert codemeta['version'] == ssnolib.__version__

    def test_readme(self):
        """checking if the version in the README.md is the same as the one of the toolbox"""

        with open(__this_dir__ / '../README.md', 'r') as f:
            readme = f.read()

        assert "ssno-1.3.0-orange" in readme

    def test_ssno_url_exists(self):
        """checking if the ssno url exists"""
        _version = ssnolib.__version__.split('.')
        _ssno_version = f'{_version[0]}.{_version[1]}.{_version[2]}'
        ssno_url = f'https://matthiasprobst.github.io/ssno/{_ssno_version}/'
        import requests
        assert requests.get(ssno_url).status_code == 200
