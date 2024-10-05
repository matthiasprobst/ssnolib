import pathlib
import re
import warnings
from typing import List, Union, Dict, Optional, Tuple

import rdflib
from ontolutils import namespaces, urirefs, Thing
from ontolutils.namespacelib.m4i import M4I
from pydantic import field_validator, Field, HttpUrl, ValidationError
from rdflib import URIRef

from ssnolib.dcat import Dataset, Distribution
from ssnolib.prov import Person, Organization, Attribution
from . import config
from . import plugins
from .namespace import SSNO
from .qudt.utils import iri2str
from .standard_name import StandardName, VectorStandardName, ScalarStandardName

MAX_ITER = 1000
__this_dir__ = pathlib.Path(__file__).parent
ROLE_LOOKUP: Dict[str, str] = {
    str(M4I.ContactPerson): "Contact person",
    str(M4I.Other): "Other person",
    str(M4I.Producer): "Producer",
    str(M4I.ProjectLeader): "Project leader",
    str(M4I.ProjectManager): "Project manager",
    str(M4I.ProjectMember): "Project member",
    str(M4I.RegistrationAgency): "Registration agency",
    str(M4I.RegistrationAuthority): "RegistrationAuthority",
    str(M4I.RelatedPerson): "Related person",
    str(M4I.ResearchGroup): "Research group",
    str(M4I.Researcher): "Research group",
    str(M4I.RightsHolder): "Rights holder",
    str(M4I.Sponsor): "Sponsor",
    str(M4I.Supervisor): "Supervisor",
    str(M4I.WorkPackageLeader): "Workpackage leader",
}


def _generate_ordered_list_of_qualifications(qres):
    sorted_list = ['https://matthiasprobst.github.io/ssno#AnyStandardName', ]
    i = 0
    while len(qres) > 0:
        i += 1
        if i > MAX_ITER:
            raise RuntimeError("Maximum number of iteration reached. There seems to be a problem with the "
                               "before/after definition. Please consult the documentation or open an issue"
                               "on github: https://github.com/matthiasprobst/ssnolib/issues/new.")
        for k, v in qres.copy().items():
            if v["before"]:
                if v["before"] in sorted_list:
                    # find the element corresponding to v["before"]:
                    i = sorted_list.index(v["before"])
                    sorted_list.insert(i, k)
                    qres.pop(k)
                # elif str(v["before"]) in (str(SSNO.AnyStandardName), str(SSNO.AnyScalarStandardName)):
                #     i = sorted_list.index('https://matthiasprobst.github.io/ssno#AnyStandardName')
                #     sorted_list.insert(i, k)
                #     qres.pop(k)

            elif v["after"]:
                if v["after"] in sorted_list:
                    i = sorted_list.index(v["after"])
                    sorted_list.insert(i + 1, k)
                    qres.pop(k)
                # elif str(v["after"]) in (str(SSNO.AnyStandardName), str(SSNO.AnyScalarStandardName)):
                #     i = sorted_list.index('https://matthiasprobst.github.io/ssno#AnyStandardName')
                #     sorted_list.insert(i + 1, k)
                #     qres.pop(k)
    return sorted_list


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
@urirefs(AnnotatedValue='ssno:AnnotatedValue',
         value='ssno:value',
         annotation='ssno:annotation')
class AnnotatedValue(Thing):
    value: str
    annotation: str


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Qualification='ssno:Qualification',
         before='ssno:before',
         after='ssno:after',
         hasPreposition='ssno:hasPreposition',
         hasValidValues='ssno:hasValidValues')
class Qualification(StandardNameModification):
    """Implementation of ssno:Qualification"""
    before: Optional[Union[str, HttpUrl, "Qualification"]] = None  # ssno:before
    after: Optional[Union[str, HttpUrl, "Qualification"]] = None  # ssno:after
    hasPreposition: Optional[str] = None  # ssno:hasPreposition
    hasValidValues: Optional[List[Union[str, AnnotatedValue]]] = None  # ssno:hasValidValues

    @field_validator('before')
    @classmethod
    def _before(cls, before: Union[str, HttpUrl, "Qualification"]) -> Union[str, "Qualification"]:
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
    def _after(cls, after: Union[str, HttpUrl, "Qualification"]) -> Union[str, "Qualification"]:
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

    @field_validator('hasValidValues')
    @classmethod
    def _hasValidValues(cls, hasValidValues: Optional[List[Union[str, AnnotatedValue]]] = None) -> List[AnnotatedValue]:
        if hasValidValues:
            for k, v in enumerate(hasValidValues.copy()):
                if isinstance(v, str):
                    hasValidValues[k] = AnnotatedValue(value=v, annotation="No description available.")
        return hasValidValues

    def get_full_name(self):
        if not self.hasPreposition:
            return self.name
        return f'{self.hasPreposition}_{self.name}'


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(VectorQualification='ssno:VectorQualification')
class VectorQualification(Qualification):
    """Special Qualification accounting for VectorStandardNames. Only one such Qualification
    must exist at max in a StandardNameTable!"""


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Character='ssno:Character',
         associatedWith='ssno:associatedWith'
         )
class Character(Thing):
    """Implementation of ssno:Transformation"""

    character: str  # ssno:character
    associatedWith: Union[str, HttpUrl, Qualification]  # ssno:associatedWith

    @field_validator('associatedWith', mode='before')
    @classmethod
    def _associatedWith(cls, associatedWith: Union[str, HttpUrl, Qualification]) -> str:
        if isinstance(associatedWith, str):
            assert str(associatedWith).startswith(("http", "_:"))
        if isinstance(associatedWith, Thing):
            return str(associatedWith.id)
        return associatedWith


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
         standardNames='ssno:standardNames',
         qualifiedAttribution='prov:qualifiedAttribution',
         hasModifier='ssno:hasModifier'
         )
class StandardNameTable(Dataset):
    """Implementation of ssno:StandardNameTable

    Parameters
    ----------
    title: str
        Title of the Standard Name Table (dcterms:title)
    version: str
        Version of the Standard Name Table (dcat:version)
    description: str
        Description of the Standard Name Table (dcterms:description)
    identifier: str
        Identifier of the Standard Name Table, e.g. the DOI (dcterms:identifier)
    qualifiedAttribution: Optional[Union[Attribution, List[Attribution]]]
        An Attribution holds a prov:Person (and its role) or a prov:Organization
    standardNames: List[StandardName]
        List of Standard Names (ssno:standardNames)
    hasModifier: Optional[List[Union[Qualification, Transformation]]]
        List of Qualifications and Transformations
    """
    title: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    identifier: Optional[str] = None
    # creator: Optional[Union[Person, List[Person], Organization, List[Organization]]] = None  # depr!
    qualifiedAttribution: Optional[Union[Attribution, List[Attribution]]] = Field(default=None,
                                                                                  alias="qualified_attribution")
    standardNames: Optional[List[StandardName]] = Field(default_factory=list,
                                                        alias="standard_names")  # ssno:standardNames
    hasModifier: Optional[List[Union[Qualification, Transformation]]] = Field(default=None,
                                                                              alias="has_modifier")  # ssno:hasModifier

    def __str__(self) -> str:
        if self.identifier:
            return self.identifier
        if self.title:
            return self.title
        return ''

    def append(self, field_name: str, field):
        self.__pydantic_validator__.validate_assignment(self.model_construct(), field_name, field)
        obj = getattr(self, field_name)
        if obj is None:
            setattr(self, field_name, [field, ])
            return
        if not isinstance(obj, list):
            raise TypeError("Can only append to list objects.")
        obj.append(field)
        setattr(self, field_name, obj)

    @classmethod
    def parse(cls,
              source: Union[str, pathlib.Path, Distribution],
              fmt: str = None,
              qudt_lookup: Optional[Dict[str, URIRef]] = None,
              **kwargs):
        """Call the reader plugin for the given format.
        Format will select the reader plugin to use. Currently, 'xml' is supported.

        Parameters
        ----------
        source: Union[str, pathlib.Path, Distribution]
            The source of the Standard Name Table. This can be a file path, URL or a Distribution object.
        qudt_lookup: Optional[Dict[str, URIRef]]
            Additional lookup table for QUDT units to translate string units like 'm/s' into QUDT URIs.
            The ontolutils package provides a lookup table for QUDT units but may not include all units of the
            parsed Standard Name Table. By providing this additional lookup table, the parser can translate
            the missing units into QUDT URIs.
        fmt: str=None
            The format of the source. If not provided, the format is determined based on the suffix of the source.
        kwargs
            Additional keyword arguments passed to the reader plugin.
        """
        from ontolutils.utils import qudt_units

        original_qudt_lookup = qudt_units.qudt_lookup
        if qudt_lookup:
            qudt_units.qudt_lookup.update(qudt_lookup)

        if isinstance(source, (str, pathlib.Path)):
            filename = source
            if fmt is None:
                filename = source
                fmt = pathlib.Path(source).suffix[1:].lower()
        else:
            if fmt is None:
                fmt = source.mediaType
            filename = source.download()
        reader = plugins.get(fmt, None)
        if reader is None:
            raise ValueError(
                f'No plugin found for the file. The reader was determined based on the suffix: {fmt}. '
                'You may overwrite this by providing the parameter fmt'
            )

        data: Dict = reader(filename).parse(**kwargs)

        # unfortunately, we need to remove all units which we could not parse...
        standardNames = []
        for sn in data["standardNames"].copy():
            try:
                standardNames.append(StandardName(**sn))
            except ValidationError as e:
                warnings.warn(f"Could not parse {sn}. {e}", UserWarning)
        data["standardNames"] = standardNames
        qudt_units.qudt_lookup = original_qudt_lookup
        return cls(**data)

    @field_validator('hasModifier', mode='before')
    @classmethod
    def _hasModifier(cls, modifications: List[Union[Qualification, Transformation]]) -> List[
        Union[Qualification, Transformation]]:
        qualifications = [m for m in modifications if isinstance(m, Qualification)]
        transformations = [m for m in modifications if isinstance(m, Transformation)]
        # if all(isinstance(m, Qualification) for m in modifications):
        # assign IDs to the qualifications including the ones behind after/before so that no duplicates exist!
        pyid_lookup = {}
        for q in qualifications:
            if not q.id:
                q.id = rdflib.URIRef(f"_:{rdflib.BNode()}")
            pyid_lookup[id(q)] = q
        for q in qualifications:
            if q.before:
                if isinstance(q.before, Qualification):
                    q.before = pyid_lookup[id(q.before)].id
                elif isinstance(q.before, str):
                    assert str(q.before).startswith(("_:", "http")), "Not a URIRef"
            if q.after:
                if isinstance(q.after, Qualification):
                    q.after = pyid_lookup[id(q.after)].id
                elif isinstance(q.after, str):
                    assert str(q.after).startswith(("_:", "http")), "Not a URIRef"
        # at max one VectorQualification!:
        nvq = len([q for q in qualifications if isinstance(q, VectorQualification)])
        if nvq > 1:
            raise ValueError("Only maximal one VectorQualification is allowed in a StandardNameTable.")
        for q in qualifications:
            if q.before is None and q.after is None:
                raise ValueError(f"Neither before nor after property is given for {q.name}")
        qualifications.extend(transformations)
        return qualifications

    @field_validator('standardNames', mode='before')
    @classmethod
    def _standard_names(cls, standardNames: Union[StandardName, List[StandardName]]) -> List[StandardName]:
        if not isinstance(standardNames, list):
            return [standardNames]
        return standardNames

    def verify_name(self, standard_name: str):
        """Verifies a string standard name"""
        # first some technical checks: must not start with a "_" etc.
        general_pattern = config.standard_name_core_pattern
        if not re.match(general_pattern, standard_name):
            print("General pattern not matched. Must be lowercase and parts may be separated by '_'.")
            return False

        if self.standardNames is None:
            return False  # no standard names exist!

        standard_name_dict = {sn.standardName: sn for sn in self.standardNames}

        str_standard_names = list(standard_name_dict.keys())

        if standard_name in str_standard_names:
            return True

        hasModifier = self.hasModifier or []
        qdict = {q.id: q for q in hasModifier if isinstance(q, Qualification)}
        regex_pattern, qualifications = self.get_qualification_regex()

        for existing_standard_name in str_standard_names:
            if existing_standard_name in standard_name:
                # found a corresponding core standard name. replace it in regex pattern:
                pattern = rf'{regex_pattern.replace("standard_name", existing_standard_name)}'

                if re.match(pattern, standard_name):
                    groups = re.match(pattern, standard_name).groups()
                    qs = [qdict[qid] for qid in qualifications]
                    for g, q in zip(groups, qs):
                        if g:
                            if isinstance(q, VectorQualification):
                                # A VectorQualification can only qualify a VectorStandardName:
                                if not isinstance(standard_name_dict[existing_standard_name], VectorStandardName):
                                    return False

                            for s in self.standardNames:
                                if s.standardName == existing_standard_name:
                                    break
                    return True
                return False
        return False

    def verify(self, standard_name: StandardName):
        """Verifies a string standard name"""
        # first some technical checks: must not start with a "_" etc.
        if not re.match(config.standard_name_core_pattern, standard_name.standardName):
            print("General pattern not matched. Must be lowercase and parts may be separated by '_'.")
            return False
        str_standard_names = [sn.standardName for sn in self.standardNames]
        str_standard_name = standard_name.standardName
        if str_standard_name in str_standard_names:
            return True
        regex_pattern, _ = self.get_qualification_regex()
        for existing_standard_name in str_standard_names:
            if existing_standard_name in str_standard_name:
                reference_canonical_units = self.get_standard_name(existing_standard_name).unit
                if standard_name.unit != reference_canonical_units:
                    raise ValueError("Canonical units do not match the reference standard name.")
                # found a corresponding core standard name. replace it in regex pattern:
                pattern = rf'{regex_pattern.replace("standard_name", existing_standard_name)}'

                if re.match(pattern, str_standard_name):
                    return True
                return False
        return False

    def get_standard_name(self, standard_name: str) -> Union[StandardName, None]:
        """Check if the Standard Name Table has a given standard name. If the name is not found it will be checked
        if it can be constructed using the qualification objects. Otherwise, None is returned.

        Parameters
        ----------
        standard_name: str
            The standard name to look for, which may be a modification of an existing one in the table.

        Returns
        -------
        Union[StandardName, None]
            The standard name object if found or constructed, otherwise None
        """
        for sn in self.standardNames:
            if sn.standardName == standard_name:
                return sn
        # let's try to construct the standard name:
        if not re.match(config.standard_name_core_pattern, standard_name):
            print("General pattern not matched. Must be lowercase and parts may be separated by '_'.")
            return None

        hasModifier = self.hasModifier or []
        qdict = {q.id: q for q in hasModifier if isinstance(q, Qualification)}
        regex_pattern, qualifications = self.get_qualification_regex()
        for existing_standard_name in self.standardNames:
            if existing_standard_name.standardName == standard_name:
                return existing_standard_name  # identical match

            if existing_standard_name.standardName in standard_name:
                # found a corresponding core standard name. replace it in regex pattern:
                core_standard_name: StandardName = existing_standard_name
                pattern = rf'{regex_pattern.replace("standard_name", existing_standard_name.standardName)}'
                if re.match(pattern, standard_name):
                    groups = re.match(pattern, standard_name).groups()
                    qs = [qdict[qid] for qid in qualifications]
                    q_description = ""
                    for g, q in zip(groups, qs):
                        if g:
                            for s in self.standardNames:
                                if s.standardName == existing_standard_name.standardName:
                                    q_description = q.description
                    return StandardName(standardName=standard_name, unit=core_standard_name.unit,
                                        description=core_standard_name.description + q_description)
        raise ValueError(
            f"The standard name {standard_name} is not part of the table and does not conform to the qualification rules.")

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
        with open(filename, 'w', encoding='utf-8') as f:
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
                        _modification.pop('after', None)
                        _modification.pop('before', None)
                        yaml_data['qualifications']['phrases'].append(_modification)
                    elif isinstance(modification, Transformation):
                        if 'transformations' not in yaml_data:
                            yaml_data['transformations'] = []
                        _modification = modification.model_dump(exclude_none=True)
                        _modification.pop('id')
                        yaml_data['transformations'].append(_modification)

            if self.standardNames:
                yaml_data['standardNames'] = {}
                for sn in self.standardNames:
                    yaml_data['standardNames'][sn.standardName] = {
                        'unit': sn.unit,
                        'description': sn.description}

            yaml.dump(yaml_data, f, sort_keys=False)

        return pathlib.Path(filename)

    def get_qualification_regex(self) -> Tuple[str, List[str]]:
        hasModifier = self.hasModifier or []
        qualifications = {m.id: m for m in hasModifier if isinstance(m, Qualification)}
        g = rdflib.Graph()
        g.parse(data=self.model_dump_jsonld(),
                format='json-ld')

        query = """
                PREFIX ssno: <https://matthiasprobst.github.io/ssno#>
                PREFIX schema: <http://schema.org/>

                SELECT ?qualification ?name ?before ?after ?preposition
                WHERE {
                    {
                        ?qualification a ssno:Qualification ;
                                       schema:name ?name .
                    } UNION {
                        ?qualification a ssno:VectorQualification ;
                                       schema:name ?name .
                    }
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
                qres[str(row.qualification).strip("_:")] = {
                    'id': row.qualification.n3(),
                    'name': str(row.name) if row.name else None,
                    'before': str(row.before).strip("_:") if row.before else None,
                    'after': str(row.after).strip("_:") if row.after else None,
                    'preposition': str(row.preposition) if row.preposition else None
                }

        qres_orig = qres.copy()
        sorted_list = _generate_ordered_list_of_qualifications(qres)

        qualification_dict = {}
        qualifications_output = []
        for e in sorted_list:
            if e in qres_orig:
                # q = qres_orig[e]
                qualifications_output.append(f'{qres_orig[e]["id"]}')
            else:
                qualifications_output.append("standard_name")
        out = ""
        for q in qualifications_output:
            qualification = qualifications.get(q, None)
            if qualification:
                valid_values = [v.value for v in qualification.hasValidValues]
                if qualification.hasPreposition:
                    _valid_values = [qualification.hasPreposition + "_" + v for v in valid_values]
                    out += f'(?:({"|".join(_valid_values)}))?_?'
                else:
                    out += f'(?:({"|".join(valid_values)}))?_?'
            elif q == "standard_name":
                out += f"{q}_?"
        qualifications_output.remove("standard_name")
        if out.endswith("?_?"):
            return "^" + out.strip("?_?") + "?$", qualifications_output
        return "^" + out + "$", qualifications_output

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
                    {
                        ?qualification a ssno:Qualification ;
                                       schema:name ?name .
                    } UNION {
                        ?qualification a ssno:VectorQualification ;
                                       schema:name ?name .
                    }
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
                qres[str(row.qualification).strip("_:")] = {
                    'name': str(row.name) if row.name else None,
                    'before': str(row.before).strip("_:") if row.before else None,
                    'after': str(row.after).strip("_:") if row.after else None,
                    'preposition': str(row.preposition) if row.preposition else None
                }

        qres_orig = qres.copy()
        sorted_list = _generate_ordered_list_of_qualifications(qres)

        qualifications_output = []
        for e in sorted_list:
            if e in qres_orig:
                q = qres_orig[e]
                if q["preposition"]:
                    qualifications_output.append(f'[{q["preposition"].replace("_", " ")} {q["name"]}]')
                else:
                    qualifications_output.append(f'[{qres_orig[e]["name"]}]')
            else:
                qualifications_output.append("standard_name")
        return " ".join(qualifications_output)

    def add_new_standard_name(self, name: Union[str, StandardName], verify: bool = True) -> StandardName:
        """Add a new standard name to the Standard Name Table.

        Parameters
        ----------
        name: Union[str, StandardName]
            The new standard name to add.
        verify: bool=True
            Verify the new standard name against the existing standard names. If False, it
            is interpreted as a new core standard name

        Returns
        -------
        StandardName
            The new StandardName object
        """
        if not verify and isinstance(name, StandardName):
            self.append("standardNames", name)
        if isinstance(name, StandardName):
            self.verify(name)
            self.append("standardNames", name)
            return name

        new_standard_name = StandardName(standardName=name, unit="dimensionless", description="N.A")

        name = new_standard_name.standardName

        for sn in self.standardNames:
            if name == sn.standardName:
                raise ValueError(f"Standard Name '{name}' already exists in the Standard Name Table.")
        if not self.verify_name(name):
            raise ValueError(f"Standard Name '{name}' is invalid. Could not verified by the qualification rules")

        return new_standard_name

    def fetch(self):
        """Download the Standard Name Table and parse it"""

    # exports
    def to_markdown(self, filename: Optional[Union[str, pathlib.Path]] = None):
        """Export the Standard Name Table to a markdown file.

        Parameters
        ----------
        filename: Optional[Union[str, pathlib.Path]]
            The filename to write the markdown file to. If None, the markdown will be printed to the console.
        """
        if filename is None:
            filename = f"{self.title}.md"
        markdown_filename = pathlib.Path(filename)

        if self.qualifiedAttribution:
            if isinstance(self.qualifiedAttribution, list):
                qualified_attribution = self.qualifiedAttribution
            else:
                qualified_attribution = [self.qualifiedAttribution, ]

            lines = []
            for qa in qualified_attribution:
                if qa.hadRole:
                    role = ROLE_LOOKUP.get(str(qa.hadRole), str(qa.hadRole).rsplit("/", 1)[-1])
                    lines.append(f"{role}: {qa.agent.to_text()}")
                else:
                    lines.append(f"Contact: {qa.agent.to_text()}")
            qatxt = '<br>\n'.join(lines)
        else:
            qatxt = None

        with open(markdown_filename, 'w', encoding="utf-8") as f:
            f.write(f"\n---\n")
            f.write(f"title: {self.title}")
            f.write(f"\n---\n\n")
            f.write(f"\n# {self.title}\n\n")
            if self.version:
                f.write(f"Version: {self.version}\n")
            if self.creator:
                if not isinstance(self.creator, list):
                    creators = [self.creator]
                else:
                    creators = self.creator

                creators_string_list = []
                for creator in creators:
                    creator_string = ""
                    if isinstance(creator, Person):
                        first_name = creator.firstName
                        last_name = creator.lastName
                        email = creator.mbox
                        affiliation = creator.affiliation
                        orcid = creator.orcidId
                        if first_name and last_name:
                            creator_string += f"{last_name}, {first_name}; "
                        if affiliation:
                            creator_string += f"{affiliation}; "
                        if email:
                            creator_string += f"{email}; "
                        if orcid:
                            creator_string += f"ORCID: {orcid}; "
                    elif isinstance(creator, Organization):
                        name = creator.name
                        url = creator.url
                        ror = creator.hasRorId
                        email = creator.mbox
                        if name:
                            creator_string += f"{name}; "
                        if url:
                            creator_string += f"{url}; "
                        if ror:
                            creator_string += f"ROR ID: {ror}; "
                        if email:
                            creator_string += f"{email}; "
                    creators_string_list.append(creator_string)
                creators_string = ', '.join(creators_string_list)
                f.write(f"<br>Creator: {creators_string.strip('; ')}\n")

            if qatxt:
                f.write(f"<br>{qatxt}\n")

            if self.description:
                f.write(f"\n\n## Description:\n\n{self.description}\n\n")

            f.write(f"\n\n\n## Modifications\n\n")
            f.write("Standard names can be modified by qualifications and transformations. Qualification do not change "
                    "the unit of a standard name, where a transformation may change the unit.")

            f.write(f"\n\n\n### Qualification\n\n")
            hasModifier = self.hasModifier or []
            qualifications = [m for m in hasModifier if isinstance(m, Qualification)]
            if qualifications:
                qualification_expl_string = self.get_qualification_rule_as_string()
                for q in qualifications:
                    if q.hasPreposition:
                        prep_str = q.hasPreposition.replace("_", " ")
                        qualification_expl_string = qualification_expl_string.replace(f"[{prep_str} {q.name}]",
                                                                                      f"[{prep_str} [{q.name}]]")
                    else:
                        qualification_expl_string = qualification_expl_string.replace(f"[{q.name}]", f"[[{q.name}]]")

                f.write(f"{qualification_expl_string}\n")
                for q in qualifications:
                    f.write(f"\n\n#### {q.name.capitalize()}\n")
                    f.write(f"Valid values: {', '.join([v.value for v in q.hasValidValues])}\n")
                    if q.description:
                        f.write(f"\n{q.description}\n")
                    else:
                        f.write("No description available.\n")
            else:
                f.write("No qualifications defined for this table.\n")

            f.write(f"\n\n### Transformations\n\n")
            transformations = [m for m in hasModifier if isinstance(m, Transformation)]
            if transformations:
                f.write(f"| Rule | Units | Meaning |\n")
                f.write(f"|---------------|:-------------|:------------|\n")
                for t in transformations:
                    f.write(f"| {t.name} | {t.altersUnit if t.altersUnit else 'N.A'} | "
                            f"{t.description if t.description else 'N.A'} |\n")
            else:
                f.write("No transformations defined for this table.\n")

            f.write(f"\n\n\n## Standard Names\n\n")

            if self.standardNames:
                f.write(f"| Standard Name | Vector/Scalar |     Units     | Description |\n")
                f.write(f"|---------------|:-------------:|:--------------|:------------|\n")

                sorted_standard_names = sorted(self.standardNames, key=lambda x: x.standardName)
                for sn in sorted_standard_names:
                    units = iri2str.get(str(sn.unit), str(sn.unit))
                    if units is None:
                        units = 'dimensionless'
                    if units == 'None':
                        units = 'dimensionless'
                    if isinstance(sn, VectorStandardName):
                        f.write(f'| {sn.standardName} | Vector | {units} | {sn.description} |\n')
                    elif isinstance(sn, ScalarStandardName):
                        f.write(f'| {sn.standardName} | Scalar | {units} | {sn.description} |\n')
                    else:
                        f.write(f'| {sn.standardName} | ? | {units} | {sn.description} |\n')
            else:
                f.write("No standard names defined for this table.\n")
        return markdown_filename

    def to_html(self,
                *,
                folder: Optional[Union[str, pathlib.Path]] = None,
                filename: Optional[Union[str, pathlib.Path]] = None) -> pathlib.Path:
        """Generates an HTML page for the standard name table.
        Either a folder or a filename may be provided. If only a folder is provided, the filename will be the title of
        the standard name table and will be saved in the folder. If only a filename is provided, the file will be saved
        wherever the filename points to. If both are provided, a ValueError is raised.

        Note
        ----
        The function requires the package "pypandoc" to be installed.

        Parameters
        ----------
        folder: Optional[Union[str, pathlib.Path]]
            The folder to save the HTML file to if the filename is not provided.
        filename: Optional[Union[str, pathlib.Path]]
            The filename to save the HTML file to if the folder is not provided.

        Returns
        -------
        pathlib.Path
            The filename of the written file.
        """
        if folder is not None and filename is not None:
            raise ValueError("Either provide a folder or a filename, not both.")
        if folder:
            assert pathlib.Path(folder).is_dir(), f"Folder {folder} is not a folder."
            assert pathlib.Path(folder).exists(), f"Folder {folder} does not exist."
            filename = pathlib.Path(folder) / f"{self.title}.html"
        if filename is None:
            filename = f"{self.title}.html"
        html_filename = pathlib.Path(filename)
        markdown_filename = self.to_markdown(html_filename.with_suffix('.tmp.md'))
        template_filename = __this_dir__ / 'templates' / 'standard_name_table.html'

        if not template_filename.exists():
            raise FileNotFoundError(f'Could not find the template file at {template_filename.absolute()}')

        # Convert Markdown to HTML using pandoc
        try:
            import pypandoc
        except ImportError:
            raise ImportError('Package "pypandoc" is required for this function.')
        output = pypandoc.convert_file(str(markdown_filename.absolute()), 'html', format='md',
                                       extra_args=['--template', template_filename])
        markdown_filename.unlink(missing_ok=True)

        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(output)

        return html_filename
