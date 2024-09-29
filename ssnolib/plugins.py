import abc
import logging
import pathlib
import warnings
from typing import Dict, Union

logger = logging.getLogger("ssnolib")


class TableReader(abc.ABC):
    """Abstract Standard Name Table Reader"""

    def __init__(self, filename: Union[str, pathlib.Path]):
        self.filename = pathlib.Path(filename)
        assert self.filename.exists(), f'{self.filename} does not exist'
        assert self.filename.is_file(), f'{self.filename} is not a file'

    @abc.abstractmethod
    def parse(self, **kwargs) -> Dict:
        """Parse the file"""


class XMLReader(TableReader):

    def parse(self, make_standard_names_lowercase: bool = False) -> Dict:
        """Parse the file"""
        try:
            import xmltodict
        except ImportError:
            raise ImportError('Package "xmltodict" is missing, but required to import from XML files.')

        with open(str(self.filename), 'r', encoding='utf-8') as file:
            my_xml = file.read()
        xmldict = xmltodict.parse(my_xml)
        _name = list(xmldict.keys())[0]

        xmldata = xmldict[_name]

        def _parse_standard_name(sndict):
            canonicalUnits = sndict.get('canonicalUnits', '')
            if canonicalUnits == '1':
                canonicalUnits = ''
            elif canonicalUnits is None:
                canonicalUnits = ''
            description = sndict.get('description', '')
            if description is None:
                description = ''
            standard_name = sndict.get('@id')
            assert standard_name is not None, 'Expected key "@id" in the XML file.'
            assert canonicalUnits is not None, 'Expected key "canonicalUnits" in the XML file.'
            assert description is not None, 'Expected key "description" in the XML file.'
            return dict(standardName=standard_name.lower() if make_standard_names_lowercase else standard_name,
                        canonicalUnits=canonicalUnits,
                        description=description)

        version = xmldata.get('version', None)
        if version is None:
            version = xmldata.get('version_number', None)

        # last_modified = xmldata.get('last_modified', None)

        contact = xmldata.get('contact', None)
        institution = xmldata.get('institution', None)
        if "@" in contact and institution is not None:
            # it is an email address
            from ssnolib.prov import Organization
            creator = Organization(mbox=contact, name=institution)
        else:
            creator = contact

            # else cannot be parsed

        sn_data = xmldata.get('entry', None)
        if sn_data is None:
            raise KeyError('Expected key "entry" in the XML file.')
        data = {'standard_name': [_parse_standard_name(sn) for sn in sn_data],
                'version': version,
                # 'modified': last_modified,
                'creator': creator}

        if 'title' not in xmldata:
            data['title'] = self.filename.stem

        sndata = data.pop('standard_name')
        for sn in sndata:
            if sn['description'] is None:
                name = sn['standard_name']
                warnings.warn(f'Description of "{name}" is None. Setting to empty string.', UserWarning)
                sn['description'] = ""
        data['standardNames'] = sndata
        return data


class YAMLReader(TableReader):

    def parse(self, **kwargs):
        try:
            import yaml
        except ImportError as e:
            raise ImportError('Package "pyyaml" is missing, but required to import from YAML files.') from e

        with open(self.filename, 'r') as f:
            data = yaml.safe_load(f)
        standardNames = data.get('standardNames', {})

        def _parse_standard_names(name, sndata: Dict):
            for ustr in ('unit', 'units', 'canonical_unit'):
                if ustr in sndata:
                    sndata['canonicalUnits'] = sndata.pop(ustr)
                    break
            _data = {'standard_name': name,
                     **sndata
                     }
            for k in list(_data.keys()):
                if k not in ('canonicalUnits', 'description', 'standard_name'):
                    _data.pop(k)
            return _data

        creator = data.get('creator', None)
        # make the orcid id the ID of the creator:
        if creator:
            if isinstance(creator, list):
                for ic, c in enumerate(creator.copy()):
                    if c['orcid_id']:
                        creator[ic]['id'] = c['orcid_id']
            else:
                if creator['orcid_id']:
                    creator['id'] = creator['orcid_id']

        # parse qualifications
        qualification_data = data.get('qualifications', None)
        qualifications_dict = {}
        if qualification_data:
            construction = qualification_data.pop('construction', None)
            if construction is None:
                logger.error("No construction string is provided in the qualifications.")
            phrases = qualification_data.get('phrases', None)
            if phrases:
                from ssnolib.standard_name_table import Qualification
                qualifications = [Qualification(
                    name=q['name'],
                    description=q.get('description', None),
                    hasPreposition=q.get('hasPreposition', None),
                    hasValidValues=q.get('hasValidValues', None)
                ) for q in phrases]
                qualifications_dict = {q.get_full_name(): q for q in qualifications}
            else:
                logger.error("No phrases are provided in the qualifications.")

            if phrases and qualifications_dict:
                from ssnolib.utils import gpfqcs
                positions = gpfqcs(construction)
                for position, q_full_name in positions.items():
                    if position < 0:
                        if position == -1:
                            from ssnolib.namespace import SSNO
                            qualifications_dict[q_full_name].before = SSNO.AnyStandardName
                        else:
                            qualifications_dict[q_full_name].before = qualifications_dict[position + 1]
                    else:
                        if position == 1:
                            from ssnolib.namespace import SSNO
                            qualifications_dict[q_full_name].after = SSNO.AnyStandardName
                        else:
                            qualifications_dict[q_full_name].after = qualifications_dict[position - 1]

                # relate the phrases to each other
                # [component] standard_name [in_medium]
                # -1, 0, 1

        data_dict = {'title': data.get('name', data.get('title', None)),
                     'creator': creator,
                     'version': data.get('version', None),
                     'description': data.get('description', None),
                     'identifier': data.get('identifier', None),
                     'standardNames': [_parse_standard_names(k, v) for k, v in standardNames.items()]}
        if qualifications_dict:
            data_dict['hasModifier'] = list(qualifications_dict.values())
        if data.get('identifier', None):
            data_dict['id'] = data.get('identifier', None)

        return data_dict


class JSONLDReader(TableReader):
    def parse(self, **kwargs) -> Dict:
        from .standard_name_table import StandardNameTable
        with open(self.filename, 'r') as f:
            import json
            snt = StandardNameTable.from_jsonld(data=json.load(f), limit=1)
            return snt.model_dump(exclude_none=True)


_plugins = {
    'xml': XMLReader,
    'text/xml': XMLReader,
    'https://www.iana.org/assignments/media-types/text/xml': XMLReader,
    'https://www.iana.org/assignments/media-types/application/xml': XMLReader,
    'yaml': YAMLReader,
    'yml': YAMLReader,
    'application/yaml': YAMLReader,
    'https://www.iana.org/assignments/media-types/application/yaml': YAMLReader,
    'jsonld': JSONLDReader,
    'application/json-ld': JSONLDReader,
    'https://www.iana.org/assignments/media-types/application/ld+json': JSONLDReader
}


def get(plugin_name: str, default=None) -> Union[TableReader, None]:
    """Returns the plugin"""
    plugin = _plugins.get(str(plugin_name), None)
    if plugin is None:
        return default
    return plugin
