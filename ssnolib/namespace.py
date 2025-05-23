from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef


class SSNO(DefinedNamespace):
    # uri = "https://matthiasprobst.github.io/ssno#"
    # Generated with ssnolib
    Character: URIRef  # ['Charakter']
    DomainConceptSet: URIRef  # ['Domain Concept Set']
    Qualification: URIRef  # ['Qualification']
    ScalarStandardName: URIRef  # ['Scalar Standard Name']
    StandardName: URIRef  # ['Standard Name']
    StandardNameModification: URIRef  # ['Standard Name Modification']
    StandardNameTable: URIRef  # ['Standard NameTable']
    Transformation: URIRef  # ['Transformation']
    VectorQualification: URIRef  # ['Vector Qualification']
    VectorStandardName: URIRef  # ['Vector Standard Name']
    after: URIRef  # ['after']
    alias: URIRef  # ['alias']
    associatedWith: URIRef  # ['associated with']
    before: URIRef  # ['before']
    dataset: URIRef  # ['dataset']
    hasCharacter: URIRef  # ['has character']
    hasDomainConceptSet: URIRef  # ['has domain concept set']
    hasModifier: URIRef  # ['has modifier']
    hasStandardName: URIRef  # ['has standard name']
    hasValidValues: URIRef  # ['has valid values']
    isStandardNameOf: URIRef  # ['is standard name of']
    positioned: URIRef  # ['positioned']
    standardNameTable: URIRef  # ['standard name table']
    standardNameTableUsedBy: URIRef  # ['standard name table used by']
    standardNames: URIRef  # ['standard names']
    unit: URIRef  # ['unit']
    usesStandardNameTable: URIRef  # ['uses standard name table']
    altersUnit: URIRef  # ['alters unit']
    ancillaryVariables: URIRef  # ['ancillary variables']
    character: URIRef  # ['character']
    description: URIRef  # ['description']
    hasPreposition: URIRef  # ['has preposition']
    longName: URIRef  # ['long name']
    standardName: URIRef  # ['standard name']
    standardNameCharacter: URIRef  # ['standard name character']
    AnyStandardName: URIRef  # ['Any Standard Name']
    AnyUnit: URIRef  # ['any unit']

    _NS = Namespace("https://matthiasprobst.github.io/ssno#")


setattr(SSNO, "Charakter", SSNO.Character)
setattr(SSNO, "Domain_Concept_Set", SSNO.DomainConceptSet)
setattr(SSNO, "Qualification", SSNO.Qualification)
setattr(SSNO, "Scalar_Standard_Name", SSNO.ScalarStandardName)
setattr(SSNO, "Standard_Name", SSNO.StandardName)
setattr(SSNO, "Standard_Name_Modification", SSNO.StandardNameModification)
setattr(SSNO, "Standard_NameTable", SSNO.StandardNameTable)
setattr(SSNO, "Transformation", SSNO.Transformation)
setattr(SSNO, "Vector_Qualification", SSNO.VectorQualification)
setattr(SSNO, "Vector_Standard_Name", SSNO.VectorStandardName)
setattr(SSNO, "after", SSNO.after)
setattr(SSNO, "alias", SSNO.alias)
setattr(SSNO, "associated_with", SSNO.associatedWith)
setattr(SSNO, "before", SSNO.before)
setattr(SSNO, "dataset", SSNO.dataset)
setattr(SSNO, "has_character", SSNO.hasCharacter)
setattr(SSNO, "has_domain_concept_set", SSNO.hasDomainConceptSet)
setattr(SSNO, "has_modifier", SSNO.hasModifier)
setattr(SSNO, "has_standard_name", SSNO.hasStandardName)
setattr(SSNO, "has_valid_values", SSNO.hasValidValues)
setattr(SSNO, "is_standard_name_of", SSNO.isStandardNameOf)
setattr(SSNO, "positioned", SSNO.positioned)
setattr(SSNO, "standard_name_table", SSNO.standardNameTable)
setattr(SSNO, "standard_name_table_used_by", SSNO.standardNameTableUsedBy)
setattr(SSNO, "standard_names", SSNO.standardNames)
setattr(SSNO, "unit", SSNO.unit)
setattr(SSNO, "uses_standard_name_table", SSNO.usesStandardNameTable)
setattr(SSNO, "alters_unit", SSNO.altersUnit)
setattr(SSNO, "ancillary_variables", SSNO.ancillaryVariables)
setattr(SSNO, "character", SSNO.character)
setattr(SSNO, "description", SSNO.description)
setattr(SSNO, "has_preposition", SSNO.hasPreposition)
setattr(SSNO, "long_name", SSNO.longName)
setattr(SSNO, "standard_name", SSNO.standardName)
setattr(SSNO, "standard_name_character", SSNO.standardNameCharacter)
setattr(SSNO, "Any_Standard_Name", SSNO.AnyStandardName)
setattr(SSNO, "any_unit", SSNO.AnyUnit)