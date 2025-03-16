import json

import pydantic

import ssnolib
from ssnolib import StandardNameTable
from ssnolib import VectorStandardName
from ssnolib.m4i import TextVariable
from ssnolib.qudt.utils import iri2str
from ssnolib.ssno.standard_name_table import ROLE2IRI


class ErrorMessages:
    def __init__(self):
        self.messages = {}

    def add(self, e: pydantic.ValidationError):
        for errors in e.errors():
            if errors['type'] not in self.messages:
                self.messages[errors['type']] = [errors['msg']]
            else:
                self.messages[errors['type']].append(errors['msg'])


def remove_off_after_on(input_list):
    """
    Remove "off" after "on" in the input list
    """
    result = []
    skip_next = False  # Flag to skip the next item if it is an "off" after "on"

    for i in range(len(input_list)):
        if skip_next:
            skip_next = False  # Reset the flag and skip this iteration
            continue

        if input_list[i] == "on":
            result.append("on")
            # Set flag to skip the next element, since it will be "off"
            skip_next = True
        else:
            result.append(input_list[i])

    return result


def parse_authors(firstnames, last_names, had_roles, orcid_ids, mboxes):
    authors = []
    roles = []
    for (first_name, last_name, role, orcid, mbox) in zip(firstnames, last_names, had_roles, orcid_ids, mboxes):
        person_dict = dict(
            firstName=first_name if first_name != '' else None,
            lastName=last_name if last_name != '' else None,
            orcidId=orcid if orcid != '' else None,
            mbox=mbox if "@" in mbox else None
        )
        for ak, av in person_dict.copy().items():
            if av is None:
                person_dict.pop(ak)
        authors.append(ssnolib.Person(**person_dict))
        roles.append(role)
    qualified_attributions = []
    for (role, author) in zip(roles, authors):
        if role:
            qualified_attributions.append(
                ssnolib.Attribution(agent=author, hadRole=ROLE2IRI[role.lower().replace(" ", "")]))
        else:
            qualified_attributions.append(ssnolib.Attribution(agent=author))
    return qualified_attributions


def parse_organizations(names, urls, ror_ids, had_roles, mboxes):
    organizations = []
    roles = []
    for (name, url, ror_id, role, mbox) in zip(names, urls, ror_ids, had_roles, mboxes):
        organization_dict = dict(
            name=name if name != '' else None,
            url=url if url != '' else None,
            mbox=mbox if "@" in mbox else None,
            hasRorId=ror_id if ror_id != '' else None
        )
        for k, v in organization_dict.copy().items():
            if v is None:
                organization_dict.pop(k)
        organizations.append(ssnolib.Organization(**organization_dict))
        roles.append(role)
    qualified_attributions = []
    for (role, organization) in zip(roles, organizations):
        if role:
            qualified_attributions.append(ssnolib.Attribution(agent=organization,
                                                              hadRole=ROLE2IRI[role.lower()]))
        else:
            qualified_attributions.append(ssnolib.Attribution(agent=organization))
    return qualified_attributions


def fetch_form_data(request, warning_messages=None):
    if warning_messages is None:
        warning_messages = {}
    error_messages = ErrorMessages()

    qa_persons = parse_authors(
        request.form.getlist("person.firstName[]"),
        request.form.getlist("person.lastName[]"),
        request.form.getlist("person.hadRole[]"),
        request.form.getlist("person.orcidId[]"),
        request.form.getlist("person.mbox[]"),
    )
    qa_orgas = parse_organizations(
        request.form.getlist("organization.name[]"),
        request.form.getlist("organization.url[]"),
        request.form.getlist("organization.hasRorId[]"),
        request.form.getlist("organization.hadRole[]"),
        request.form.getlist("organization.mbox[]"),
    )
    has_valid_values_raw = request.form.getlist("hasValidValues[]")
    has_variable_description = request.form.getlist("hasVariableDescription[]")
    qualification_description = request.form.getlist("qualification_description[]")
    qualification_name = request.form.getlist("qualification_name[]")
    _vectors = request.form.getlist("is_vector_qualification[]")

    vector = remove_off_after_on(_vectors)

    prepositions = [p.strip() for p in request.form.getlist("preposition[]")]

    # figure out what is before and what is after the AnyStandardName:
    before_list = []
    after_list = []
    is_before_any_stdname = True
    for i, name in enumerate(qualification_name):
        if name == "AnyStandardName":
            is_before_any_stdname = False
        else:
            if is_before_any_stdname:
                before_list.append(name)
            else:
                after_list.append(name)
    before = {}
    if len(before_list) == 1:
        before = {before_list[0]: str(ssnolib.namespace.SSNO.AnyStandardName)}
    elif len(before_list) > 1:
        for i, b in enumerate(before_list[:-1]):
            before[b] = before_list[i + 1]
    after = {}
    if len(after_list) == 1:
        after = {after_list[0]: str(ssnolib.namespace.SSNO.AnyStandardName)}
    elif len(after_list) > 1:
        for i, a in enumerate(after_list[:-1]):
            after[a] = after_list[i + 1]

    qualification_name.remove("AnyStandardName")

    qualifications = []
    for name, vec, preposition, hvvr, descr in zip(qualification_name,
                                                   vector,
                                                   prepositions,
                                                   has_valid_values_raw,
                                                   qualification_description):
        prep = None if preposition == '' else preposition
        qvalues = []
        for v in hvvr.split(","):
            description = has_variable_description.pop(0)
            qvalues.append(TextVariable(hasStringValue=v.strip(), hasVariableDescription=description))
        if vec == 'on':
            qualifications.append(
                ssnolib.VectorQualification(name=name, hasValidValues=qvalues, description=descr,
                                            hasPreposition=prep)
            )
        else:
            qualifications.append(
                ssnolib.Qualification(name=name, hasValidValues=qvalues, description=descr, hasPreposition=prep)
            )

    for i, qname in enumerate(qualification_name):
        if qname in before:
            _before_value = before[qname]
            if _before_value.startswith("http"):
                qualifications[i].before = _before_value
            else:
                for q in qualifications:
                    if q.name == _before_value:
                        qualifications[i].before = q.id
        elif qname in after:
            _after_value = after[qname]
            if _after_value.startswith("http"):
                qualifications[i].after = _after_value
            else:
                for q in qualifications:
                    if q.name == _after_value:
                        qualifications[i].after = q.id
    qa_persons.extend(qa_orgas)

    standard_name_names = request.form.getlist("standard_name.name[]")
    standard_name_units = request.form.getlist("standard_name.unit[]")
    standard_name_descriptions = request.form.getlist("standard_name.description[]")
    is_vector_standard_name = remove_off_after_on(request.form.getlist("is_vector_standard_name[]"))
    standard_name_classes = [VectorStandardName if is_vector == 'on' else ssnolib.ScalarStandardName for is_vector in
                             is_vector_standard_name]
    assert len(standard_name_names) == len(standard_name_units) == len(standard_name_descriptions) == len(
        is_vector_standard_name), "Length of standard names, units, descriptions and vector flags do not match"

    standard_names = []
    for (cls, name, unit, description) in zip(standard_name_classes, standard_name_names, standard_name_units,
                                              standard_name_descriptions):
        try:
            new_sn = cls(
                standardName=name,
                unit=unit,
                description=description
            )
            standard_names.append(new_sn)
        except pydantic.ValidationError as e:
            error_messages.add(e)

    snt = StandardNameTable(
        title=request.form.get("title"),
        version=request.form.get("version"),
        description=request.form.get("description"),
        qualifiedAttribution=qa_persons,
        hasModifier=qualifications,
        standardNames=standard_names
    )
    json_data = json.loads(snt.model_dump_jsonld())

    has_errors = False
    for k, v in error_messages.messages.items():
        if len(v) > 0:
            has_errors = True
            break

    data, warning_messages = snt_to_cache_data(snt, warning_messages)

    return json_data, data, warning_messages, error_messages, has_errors


def snt_to_cache_data(snt: StandardNameTable, warning_messages):
    if not isinstance(snt.qualifiedAttribution, list):
        if snt.qualifiedAttribution is not None:
            qualified_attributions = [snt.qualifiedAttribution]
        else:
            qualified_attributions = []
    else:
        if snt.qualifiedAttribution is not None:
            qualified_attributions = snt.qualifiedAttribution
        else:
            qualified_attributions = []

    persons = []
    organizations = []
    for qualified_attribution in qualified_attributions:
        if isinstance(qualified_attribution.agent, ssnolib.Person):
            persons.append(qualified_attribution.agent.model_dump(exclude_none=True))
            if qualified_attribution.hadRole:
                persons[-1]["hadRole"] = qualified_attribution.hadRole.rsplit("#", 1)[-1]
        elif isinstance(qualified_attribution.agent, ssnolib.Organization):
            organizations.append(qualified_attribution.agent.model_dump(exclude_none=True))
            if qualified_attribution.hadRole:
                organizations[-1]["hadRole"] = qualified_attribution.hadRole.rsplit("#", 1)[-1]
    modifier = snt.hasModifier or []
    qualifications = [m for m in modifier if isinstance(m, (ssnolib.VectorQualification,
                                                            ssnolib.Qualification))]
    transformations = [m for m in modifier if isinstance(m, ssnolib.Transformation)]
    transformations_dict = [t.model_dump(exclude_none=True) for t in transformations]
    for i, transformation in enumerate(transformations):
        for j, character in enumerate(transformation.hasCharacter):
            if character.associatedWith.startswith('_:'):
                for q in qualifications:
                    if q.id == character.associatedWith:
                        transformations_dict[i]["hasCharacter"][j]["associatedWith"] = q.name
                        break

    title = snt.title
    version = snt.version
    description = snt.description
    standard_names = snt.standardNames

    standard_names_data = []
    for sn in standard_names:
        unit_str = iri2str.get(sn.unit, None)
        if unit_str is None:
            warning_messages["UnitParsWarnings"].append(
                f'Could not parse unit "{sn.unit}" of standard name "{sn.standardName}" to human readable unit.'
            )
            unit_str = sn.unit.rsplit('/', 1)[-1]
        standard_names_data.append(
            {'standardName': sn.standardName,
             'unit_str': unit_str,
             'unit': sn.unit,
             'description': sn.description,
             'is_vector': isinstance(sn, VectorStandardName)}
        )

    data = {
        'title': title,
        'version': version,
        'description': description,
        'persons': persons,
        'organizations': organizations,
        'qualifications': qualifications,
        'transformations': transformations_dict,
        'standard_names': standard_names_data
    }
    return data, warning_messages
