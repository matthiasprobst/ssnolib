import pathlib
from typing import List, Union, Dict, Optional

import rdflib
from ontolutils import namespaces, urirefs, Thing
from pydantic import field_validator, Field, HttpUrl

from ssnolib.dcat import Dataset, Distribution
from ssnolib.prov import Person, Organization
from . import plugins
from .namespace import SSNO
from .standard_name import StandardName


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            schema="http://schema.org/",
            dcterms="http://purl.org/dc/terms/")
@urirefs(StandardNameModification='ssno:StandardNameModification',
         name='schema:name',
         description='dcterms:description')
class StandardNameModification(Thing):
    """Implementation of ssno:StandardNameModification"""

    name: str  # schema:name
    description: str  # dcterms:description

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.name}")'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Qualification='ssno:Qualification',
         before='ssno:before',
         after='ssno:after',
         hasPreposition='ssno:hasPreposition',
         hasValidValues='ssno:hasValidValues')
class Qualification(StandardNameModification):
    """Implementation of ssno:Qualification"""
    before: Optional[Union[str, "Qualification"]] = None  # ssno:before
    after: Optional[Union[str, "Qualification"]] = None  # ssno:after
    hasPreposition: Optional[str] = None  # ssno:hasPreposition
    hasValidValues: Optional[List[str]] = None  # ssno:hasValidValues

    @field_validator('before')
    @classmethod
    def _before(cls, before: Union[str, "Qualification"]) -> Union[str, "Qualification"]:
        if isinstance(before, str):
            if not before.startswith("_:") and not before.startswith("http"):
                raise ValueError(f'Expected a URIRef or Qualification, got {before}')
            return before
        if isinstance(before, rdflib.URIRef):
            return str(before)
        if not isinstance(before, Qualification) and before != SSNO.AnyStandardName and before != str(
                SSNO.AnyStandardName):
            raise TypeError(f'Expected a AnyStandardName or Qualification, got {type(before)}')
        return before

    @field_validator('after')
    @classmethod
    def _after(cls, after: Union[str, "Qualification"]) -> Union[str, "Qualification"]:
        if isinstance(after, str):
            if not after.startswith("_:") and not after.startswith("http"):
                raise ValueError(f'Expected a URIRef or Qualification, got {after}')
            return after
        if isinstance(after, rdflib.URIRef):
            return str(after)
        if not isinstance(after, Qualification) and after != SSNO.AnyStandardName and after != str(
                SSNO.AnyStandardName):
            raise TypeError(f'Expected a AnyStandardName or Qualification, got {type(after)}')
        return after

    def get_full_name(self):
        if not self.hasPreposition:
            return self.name
        return f'{self.hasPreposition}_{self.name}'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Character='ssno:Character',
         character='ssno:character',
         associatedWith='ssno:associatedWith'
         )
class Character(Thing):
    """Implementation of ssno:Transformation"""

    character: str  # ssno:character
    associatedWith: Union[HttpUrl, Qualification]  # ssno:associatedWith


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Transformation='ssno:Transformation',
         altersUnit='ssno:unitModificationRule',
         hasCharacter='ssno:hasCharacter'
         )
class Transformation(StandardNameModification):
    """Implementation of ssno:Transformation"""

    altersUnit: str  # ssno:altersUnit
    hasCharacter: List[Character]  # ssno:hasCharacter


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            dcterms="http://purl.org/dc/terms/")
@urirefs(StandardNameTable='ssno:StandardNameTable',
         creator='dcterms:creator',
         standard_names='ssno:standardNames',
         hasModifier='ssno:hasModifier'
         )
class StandardNameTable(Dataset):
    """Implementation of ssno:StandardNameTable

    Parameters
    ----------
    title: str
        Title of the Standard Name Table (dcterms:title)
    description: str
        Description of the Standard Name Table (dcterms:description)
    creator: Union[Person, List[Person], Organization, List[Organization]]
        Creator of the SNT (dcterms:creator)
    version: str
        Version of the Standard Name Table (dcat:version)
    identifier: str
        Identifier of the Standard Name Table, e.g. the DOI (dcterms:identifier)
    standard_names: List[StandardName]
        List of Standard Names (ssno:standardNames)
    """
    title: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    identifier: Optional[str] = None
    creator: Optional[Union[Person, List[Person], Organization, List[Organization]]] = None
    standard_names: List[StandardName] = Field(default=None, alias="standardNames")  # ssno:standardNames
    hasModifier: List[Union[Qualification, Transformation]] = None

    def __str__(self) -> str:
        if self.identifier:
            return self.identifier
        if self.title:
            return self.title
        return ''

    @classmethod
    def parse(cls,
              source: Union[str, pathlib.Path, Distribution],
              fmt: str = None):
        """Call the reader plugin for the given format.
        Format will select the reader plugin to use. Currently, 'xml' is supported."""
        if isinstance(source, (str, pathlib.Path)):
            filename = source
            if fmt is None:
                filename = source
                fmt = pathlib.Path(source).suffix[1:].lower()
        else:
            if fmt is None:
                fmt = source.media_type
            filename = source.download()
        reader = plugins.get(fmt, None)
        if reader is None:
            raise ValueError(
                f'No plugin found for the file. The reader was determined based on the suffix: {fmt}. '
                'You may overwrite this by providing the parameter fmt'
            )

        data: Dict = reader(filename).parse()

        return cls(**data)

    @field_validator('hasModifier', mode='before')
    @classmethod
    def _defines_standard_name_modification(cls, modifications: List[Union[Qualification, Transformation]]) -> List[
        Qualification]:
        if all(isinstance(m, Qualification) for m in modifications):
            # assign IDs to the qualifications including the ones behind after/before so that no duplicates exist!
            pyid_lookup = {}
            for q in modifications:
                q.id = rdflib.URIRef(f"_:{rdflib.BNode()}")
                pyid_lookup[id(q)] = q
            for q in modifications:
                if q.before:
                    if isinstance(q.before, Qualification):
                        q.before = pyid_lookup[id(q.before)].id
                    elif isinstance(q.before, str):
                        assert str(q.before) == str(SSNO.AnyStandardName)
                if q.after:
                    if isinstance(q.after, Qualification):
                        q.after = pyid_lookup[id(q.after)].id
                    elif isinstance(q.after, str):
                        assert str(q.after) == str(SSNO.AnyStandardName)
            return modifications
        if all(isinstance(m, Transformation) for m in modifications):
            return modifications
        raise ValueError('Expected a list of either Qualifications or Transformations')

    @field_validator('standard_names', mode='before')
    @classmethod
    def _standard_names(cls, standard_names: Union[StandardName, List[StandardName]]) -> List[StandardName]:
        if not isinstance(standard_names, list):
            return [standard_names]
        return standard_names

    def get_standard_name(self, standard_name: str) -> Union[StandardName, None]:
        """Check if the Standard Name Table has a given standard name. The
        standard name object is returned if found, otherwise None.

        Parameters
        ----------
        standard_name: str
            The standard name to look for

        Returns
        -------
        Union[StandardName, None]
            The standard name object if found, otherwise None
        """
        for sn in self.standard_names:
            if sn.standard_name == standard_name:
                return sn
        return

    def to_yaml(self, filename: Union[str, pathlib.Path], overwrite: bool = False, exists_ok=False) -> pathlib.Path:
        """Dump the Standard Name Table to a file.

        Parameters
        ----------
        filename: Union[str, pathlib.Path]
            The filename to write the Standard Name Table to.
        overwrite: bool=False
            Overwrite the file if it exists.
        exists_ok: bool=False
            If the file exists, return without writing the file. Note, that the
            file content is not checked!

        Returns
        -------
        filename: pathlib.Path
            The filename of the written file.

        Raises
        ------
        ValueError
            If the file exists and overwrite is False.
        """
        import yaml
        if pathlib.Path(filename).exists() and not overwrite:
            if exists_ok:
                return pathlib.Path(filename)
            raise ValueError(f'File {filename} exists and overwrite is False.')

        suffix = pathlib.Path(filename).suffix
        assert suffix in ('.yaml', '.yml'), f'Expected a YAML file, got {suffix}'

        yaml_data = {}
        with open(filename, 'w') as f:
            if self.title:
                yaml_data['name'] = self.title
            if self.version:
                yaml_data['version'] = self.version
            if self.description:
                yaml_data['description'] = self.description
            if self.identifier:
                yaml_data['identifier'] = self.identifier

            if self.creator:
                if isinstance(self.creator, list):
                    _creators = self.creator
                else:
                    _creators = [self.creator]

                if _creators:
                    yaml_data['creator'] = []
                    for creator in _creators:
                        creator_dict = creator.model_dump(exclude_none=True)
                        if creator_dict:
                            yaml_data['creator'].append(creator_dict)
                if len(yaml_data['creator']) == 0:
                    yaml_data.pop('creator')

            if self.hasModifier:
                for modification in self.hasModifier:
                    if isinstance(modification, Qualification):
                        if 'qualifications' not in yaml_data:
                            yaml_data['qualifications'] = {
                                'construction': self.get_qualification_rule_as_string(),
                                'phrases': []
                            }

                        _modification = modification.model_dump(exclude_none=True)
                        _modification.pop('id')
                        # if _modification.get('before', None) is not None and str(_modification['before']) != str(SSNO.AnyStandardName):
                        #     for _m in self.hasModifier:
                        #         if str(_m.id) == modification.before:
                        #             _modification['before'] = _m.name
                        # elif _modification.get('after', None) is not None and str(_modification['after']) != str(SSNO.AnyStandardName):
                        #     for _m in self.hasModifier:
                        #         if str(_m.id) == modification.before:
                        #             _modification['after'] = _m.name
                        _modification.pop('after', None)
                        _modification.pop('before', None)
                        yaml_data['qualifications']['phrases'].append(_modification)
                    elif isinstance(modification, Transformation):
                        if 'transformations' not in yaml_data:
                            yaml_data['transformations'] = []
                        _modification = modification.model_dump(exclude_none=True)
                        _modification.pop('id')
                        yaml_data['transformations'].append(_modification)

            if self.standard_names:
                yaml_data['standard_names'] = {}
                for sn in self.standard_names:
                    yaml_data['standard_names'][sn.standard_name] = {'canonical_units': sn.canonical_units,
                                                                     'description': sn.description}

            # if self.locations:
            #     for loc in self.locations:
            #         yaml_data['locations'] = {loc.name: loc.description}
            #
            # if self.media:
            #     for med in self.media:
            #         yaml_data['media'] = {med.name: med.description}
            #
            # if self.conditions:
            #     for cond in self.conditions:
            #         yaml_data['conditions'] = {cond.name: cond.description}
            #
            # if self.reference_frames:
            #     for ref in self.reference_frames:
            #         yaml_data['reference_frames'] = {ref.name: ref.description}

            yaml.dump(yaml_data, f, sort_keys=False)

        # yaml_data = {'description': self.description if self.description,
        #              'identifier': }
        # print(self.model_dump())

        return pathlib.Path(filename)

    def get_qualification_rule_as_string(self) -> str:
        """Returns the qualification rule similar to the CF standard name table documentation
        (https://cfconventions.org/Data/cf-standard-names/docs/guidelines.html#process)."""
        # get all qualifications:
        g = rdflib.Graph()
        g.parse(data=self.model_dump_jsonld(),
                format='json-ld')

        query = """
                PREFIX ssno: <https://matthiasprobst.github.io/ssno#>
                PREFIX schema: <http://schema.org/>

                SELECT ?qualification ?name ?before ?after ?preposition
                WHERE {
                    ?qualification a ssno:Qualification ;
                                   schema:name ?name .
                    OPTIONAL { ?qualification ssno:before ?before }
                    OPTIONAL { ?qualification ssno:after ?after }
                    OPTIONAL { ?qualification ssno:hasPreposition ?preposition }
                }
                ORDER BY ?before
                """
        # Execute the query
        results = g.query(query)

        # Print the results
        qres = {}
        for row in results:
            if row.qualification not in qres:
                qres[str(row.qualification).strip("_:")] = {'name': str(row.name) if row.name else None,
                                                            'before': str(row.before).strip(
                                                                "_:") if row.before else None,
                                                            'after': str(row.after).strip("_:") if row.after else None,
                                                            'preposition': str(
                                                                row.preposition) if row.preposition else None}

        sorted_list = ['https://matthiasprobst.github.io/ssno#AnyStandardName', ]
        qres_orig = qres.copy()
        while len(qres) > 0:
            for k, v in qres.copy().items():
                if v["before"] in sorted_list:
                    # find the element corresponding to v["before"]:
                    i = sorted_list.index(v["before"])
                    sorted_list.insert(i, k)
                    qres.pop(k)
                elif v["after"] in sorted_list:
                    i = sorted_list.index(v["after"])
                    sorted_list.insert(i + 1, k)
                    qres.pop(k)

        qualifications_output = []
        for e in sorted_list:
            if e in qres_orig:
                q = qres_orig[e]
                if q["preposition"]:
                    qualifications_output.append(f'[{q["preposition"]}_{q["name"]}]')
                else:
                    qualifications_output.append(f'[{qres_orig[e]["name"]}]')
            else:
                qualifications_output.append("standard_name")
        return " ".join(qualifications_output)
