from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef


class SSNO(DefinedNamespace):
    # uri = "https://matthiasprobst.github.io/ssno/#"
    # Generated with ssnolib
    Qualification: URIRef  # ['Qualification']
    StandardName: URIRef  # ['StandardName']
    StandardNameModification: URIRef  # ['standard name modification']
    StandardNameTable: URIRef  # ['StandardNameTable']
    Transformation: URIRef  # ['Transformation']
    after: URIRef  # ['after']
    associatedWith: URIRef  # ['associated with']
    before: URIRef  # ['before']
    hasCharacter: URIRef  # ['has character']
    hasModifier: URIRef  # ['has modifier']
    hasStandardName: URIRef  # ['has standard name']
    isDefinedBy: URIRef  # ['is defined by']
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
    hasPreposition: URIRef  # ['has preposition']
    hasValidValues: URIRef  # ['has valid values']
    longName: URIRef  # ['long name']
    standardName: URIRef  # ['standard name']
    standardNameCharacter: URIRef  # ['standard name character']
    AnyStandardName: URIRef  # ['Any Standard Name']

    _NS = Namespace("https://matthiasprobst.github.io/ssno#")


setattr(SSNO, "Qualification", SSNO.Qualification)
setattr(SSNO, "StandardName", SSNO.StandardName)
setattr(SSNO, "standard_name_modification", SSNO.StandardNameModification)
setattr(SSNO, "StandardNameTable", SSNO.StandardNameTable)
setattr(SSNO, "Transformation", SSNO.Transformation)
setattr(SSNO, "after", SSNO.after)
setattr(SSNO, "associated_with", SSNO.associatedWith)
setattr(SSNO, "before", SSNO.before)
setattr(SSNO, "has_character", SSNO.hasCharacter)
setattr(SSNO, "has_modifier", SSNO.hasModifier)
setattr(SSNO, "has_standard_name", SSNO.hasStandardName)
setattr(SSNO, "is_defined_by", SSNO.isDefinedBy)
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
setattr(SSNO, "has_preposition", SSNO.hasPreposition)
setattr(SSNO, "has_valid_values", SSNO.hasValidValues)
setattr(SSNO, "long_name", SSNO.longName)
setattr(SSNO, "standard_name", SSNO.standardName)
setattr(SSNO, "standard_name_character", SSNO.standardNameCharacter)
setattr(SSNO, "Any_Standard_Name", SSNO.AnyStandardName)