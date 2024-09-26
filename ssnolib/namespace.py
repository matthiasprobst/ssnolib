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
    before: URIRef  # ['before']
    canonicalUnits: URIRef  # ['canonical units']
    contact: URIRef  # ['contact']
    hasModifier: URIRef  # ['defines standard name modification']
    hasStandardName: URIRef  # ['has standard name']
    isDefinedBy: URIRef  # ['is standard name modification defined in']
    isStandardNameOf: URIRef  # ['is standard name of']
    positioned: URIRef  # ['positioned']
    standardNameTable: URIRef  # ['standard name table']
    standardNameTableUsedBy: URIRef  # ['standard name table used by']
    standardNames: URIRef  # ['standard names']
    usesStandardNameTable: URIRef  # ['uses standard name table']
    altersUnit: URIRef  # ['alters unit']
    ancillaryVariables: URIRef  # ['ancillary variables']
    description: URIRef  # ['description']
    hasPreposition: URIRef  # ['has preposition']
    hasValidValues: URIRef  # ['has valid values']
    longName: URIRef  # ['long name']
    standardName: URIRef  # ['standard name']
    AnyStandardName: URIRef  # ['Any Standard Name']

    _NS = Namespace("https://matthiasprobst.github.io/ssno#")


setattr(SSNO, "Qualification", SSNO.Qualification)
setattr(SSNO, "StandardName", SSNO.StandardName)
setattr(SSNO, "standard_name_modification", SSNO.StandardNameModification)
setattr(SSNO, "StandardNameTable", SSNO.StandardNameTable)
setattr(SSNO, "Transformation", SSNO.Transformation)
setattr(SSNO, "after", SSNO.after)
setattr(SSNO, "before", SSNO.before)
setattr(SSNO, "canonicalUnits", SSNO.canonicalUnits)
setattr(SSNO, "contact", SSNO.contact)
setattr(SSNO, "defines_standard_name_modification", SSNO.hasModifier)
setattr(SSNO, "has_standard_name", SSNO.hasStandardName)
setattr(SSNO, "is_standard_name_modification_defined_in", SSNO.isDefinedBy)
setattr(SSNO, "is_standard_name_of", SSNO.isStandardNameOf)
setattr(SSNO, "positioned", SSNO.positioned)
setattr(SSNO, "standard_name_table", SSNO.standardNameTable)
setattr(SSNO, "standard_name_table_used_by", SSNO.standardNameTableUsedBy)
setattr(SSNO, "standard_names", SSNO.standardNames)
setattr(SSNO, "uses_standard_name_table", SSNO.usesStandardNameTable)
setattr(SSNO, "alters_unit", SSNO.altersUnit)
setattr(SSNO, "ancillary_variables", SSNO.ancillaryVariables)
setattr(SSNO, "description", SSNO.description)
setattr(SSNO, "has_preposition", SSNO.hasPreposition)
setattr(SSNO, "has_valid_values", SSNO.hasValidValues)
setattr(SSNO, "long_name", SSNO.longName)
setattr(SSNO, "standard_name", SSNO.standardName)
setattr(SSNO, "Any_Standard_Name", SSNO.AnyStandardName)