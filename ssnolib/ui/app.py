import json

from flask import Flask, render_template, request, redirect

import ssnolib
from ssnolib import StandardNameTable, VectorStandardName
from ssnolib.qudt.utils import iri2str
from ssnolib.standard_name_table import ROLE2IRI
from utils import remove_off_after_on
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html', data={})


@app.route('/JSON-LD', methods=['POST'])
def json_ld():
    def parseAuthors(firstnames, lastNames, hadRoles, orcidIDs, mboxes):
        authors = []
        roles = []
        for (first_name, last_name, role, orcid, mbox) in zip(firstnames, lastNames, hadRoles, orcidIDs, mboxes):
            person_dict = dict(
                firstName=first_name if first_name != '' else None,
                lastName=last_name if last_name != '' else None,
                orcidId=orcid if orcid != '' else None,
                mbox=mbox if "@" in mbox else None
            )
            for k, v in person_dict.copy().items():
                if v is None:
                    person_dict.pop(k)
            authors.append(ssnolib.Person(**person_dict))
            roles.append(role)
        qualifiedAttributions = []
        for (role, author) in zip(roles, authors):
            if role:
                qualifiedAttributions.append(ssnolib.Attribution(agent=author, hadRole=ROLE2IRI[role.lower()]))
            else:
                qualifiedAttributions.append(ssnolib.Attribution(agent=author))
        return qualifiedAttributions

    def parseOrganizations(names, urls, rorIDs, hadRoles, mboxes):
        organizations = []
        roles = []
        for (name, url, rorID, role, mbox) in zip(names, urls, rorIDs, hadRoles, mboxes):
            organization_dict = dict(
                name=name if name != '' else None,
                url=url if url != '' else None,
                role=role if role != '' else None,
                mbox=mbox if "@" in mbox else None
            )
            for k, v in organization_dict.copy().items():
                if v is None:
                    organization_dict.pop(k)
            organizations.append(ssnolib.Organization(**organization_dict))
            roles.append(role)
        qualifiedAttributions = []
        for (role, organization) in zip(roles, organizations):
            if role:
                qualifiedAttributions.append(ssnolib.Attribution(agent=organization, hadRole=ROLE2IRI[role.lower()]))
            else:
                qualifiedAttributions.append(ssnolib.Attribution(agent=organization))
        return qualifiedAttributions

    qa_persons = parseAuthors(
        request.form.getlist("person.firstName[]"),
        request.form.getlist("person.lastName[]"),
        request.form.getlist("person.hadRole[]"),
        request.form.getlist("person.orcidId[]"),
        request.form.getlist("person.mbox[]"),
    )
    qa_orgas = parseOrganizations(
        request.form.getlist("organization.name[]"),
        request.form.getlist("organization.url[]"),
        request.form.getlist("organization.hasRorId[]"),
        request.form.getlist("organization.hadRole[]"),
        request.form.getlist("organization.mbox[]"),
    )
    hasValidValuesRaw = request.form.getlist("hasValidValues[]")
    hasValidValuesDescription = request.form.getlist("hasValidValuesDescription[]")
    qualification_description = request.form.getlist("qualification_description[]")
    qualification_name = request.form.getlist("qualification_name[]")
    _vectors = request.form.getlist("is_vector_qualification[]")

    vector = remove_off_after_on(_vectors)

    preposition = request.form.getlist("preposition[]")

    # figure out what is before and what is after the AnyStandardName:
    beforeList = []
    afterList = []
    isBevoreAnyStandardName = True
    for i, name in enumerate(qualification_name):
        if name == "AnyStandardName":
            isBevoreAnyStandardName=False
        else:
            if isBevoreAnyStandardName:
                beforeList.append(name)
            else:
                afterList.append(name)
    before = {}
    if len(beforeList) == 1:
        before = {beforeList[0]: str(ssnolib.namespace.SSNO.AnyStandardName)}
    elif len(beforeList) > 1:
        for i, b in enumerate(beforeList[:-1]):
            before[b] = beforeList[i+1]
    after = {}
    if len(afterList) == 1:
        after = {afterList[0]: str(ssnolib.namespace.SSNO.AnyStandardName)}
    elif len(afterList) > 1:
        for i, a in enumerate(afterList[:-1]):
            after[a] = afterList[i+1]

    qualification_name.remove("AnyStandardName")

    qualifications = []
    for name, vec, preposition, hvvr, descr in zip(qualification_name, vector, preposition, hasValidValuesRaw,
                                                   qualification_description):
        qvalues = []
        for v in hvvr.split(","):
            description = hasValidValuesDescription.pop(0)
            qvalues.append(ssnolib.ValidQualificationValue(qualificationValue=v, description=description))
        if vec == 'on':
            qualifications.append(
                ssnolib.VectorQualification(name=name, hasValidValues=qvalues, description=descr,
                                        hasPreposition=preposition)
            )
        else:
            qualifications.append(
                ssnolib.Qualification(name=name, hasValidValues=qvalues, description=descr, hasPreposition=preposition)
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

    standard_name_classes = [VectorStandardName if is_vector == 'on' else ssnolib.ScalarStandardName for is_vector in is_vector_standard_name]
    assert len(standard_name_names) == len(standard_name_units) == len(standard_name_descriptions) == len(is_vector_standard_name), "Length of standard names, units, descriptions and vector flags do not match"

    standardNames = [
        cls(
            standardName=name,
            unit=unit,
            description=description
        ) for (cls, name, unit, description) in zip(standard_name_classes, standard_name_names, standard_name_units, standard_name_descriptions)
    ]

    snt = StandardNameTable(
        title=request.form.get("title"),
        version=request.form.get("version"),
        description=request.form.get("description"),
        qualifiedAttribution=qa_persons,
        hasModifier=qualifications,
        standardNames=standardNames
    )
    config_data = json.loads(snt.model_dump_jsonld())

    return render_template('jsonld.html', config_data=config_data)


@app.route('/loadJSONLD', methods=['POST'])
def loadJSONLD():
    # Get the uploaded file
    json_content = json.load(request.files['jsonld_file'])
    try:
        snt = ssnolib.parse_table(data=json_content)
        # snt = StandardNameTable.from_jsonld(data=json_content, limit=1)

        # Example of extracting data from JSON-LD
        if not isinstance(snt.qualifiedAttribution, list):
            if snt.qualifiedAttribution is not None:
                qualifiedAttribution = [snt.qualifiedAttribution]
            else:
                qualifiedAttribution = []
        else:
            if snt.qualifiedAttribution is not None:
                qualifiedAttribution = snt.qualifiedAttribution
            else:
                qualifiedAttribution = []

        persons = []
        organizations = []
        for qa in qualifiedAttribution:
            if isinstance(qa.agent, ssnolib.Person):
                persons.append(qa.agent.model_dump(exclude_none=True))
                if qa.hadRole:
                    persons[-1]["hadRole"] = qa.hadRole.rsplit("#", 1)[-1]
            elif isinstance(qa.agent, ssnolib.Organization):
                organizations.append(qa.agent.model_dump(exclude_none=True))
                if qa.hadRole:
                    organizations[-1]["hadRole"] = qa.hadRole.rsplit("#", 1)[-1]
        modifier = snt.hasModifier or []
        qualifications = [m for m in modifier if isinstance(m, (ssnolib.VectorQualification,
                                                                ssnolib.ScalarStandardName,
                                                                ssnolib.StandardName))]
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

        data = {
            'title': title,
            'version': version,
            'description': description,
            'persons': persons,
            'organizations': organizations,
            'qualifications': qualifications,
            'transformations': transformations_dict,
            'standard_names': [
                {'standardName': sn.standardName, 'unit_str': iri2str.get(sn.unit, 'N.A.'), 'unit': sn.unit,
                 'description': sn.description,
                 'is_vector': isinstance(sn, VectorStandardName)} for sn
                in standard_names]
        }

        # Render the form with pre-filled data
        return render_template('form.html', data=data)
    except Exception as e:
        pass
    # Redirect back to the welcome page if the file is not valid
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
