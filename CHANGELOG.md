# CHANGELOG

Log of changes in the versions

## v1.5.1.4

- update `to_xml`
- dcat:Distribution allows foaf-Agents as creators
- fix StandardNameTable version property. `hasVersion` was used wrongly as a string, now it is a resource and
  `schema:version` is added for the current version.
- using `LangString` in multiple objects to allow language-sensitive strings

## v1.5.1.3

- upgrade to ontolutils v0.19.2
- it is enforced to use base-uri (e.g. a DOI URL) when calling `to_jsonld()` from `StandardNameTable` to ensure that the
  standard
  names
  are unique
- add `skos.Note`
- bugfix `hasDomainConceptSet`
- bugfix downloading Table via Distribution.

## v1.5.1.2

- correctly testing vector qualifications
- improve on description generation when constructing a standard name from qualifications
- drop support for Python 3.8

## v1.5.1.1

- add dependency `pint`

## v1.5.1.0

- Qualification is subclass of `DomainConceptSet` and `StandardNameModification`
- add readthedocs documentation: https://ssnolib.readthedocs.io/en/latest/index.html

## v1.5.0.1

- Hotfix determine standard name

## v1.5.0.0

- `Collection` is added to allow constructing transformations that use terms, that are not of type `Qualification`
- min `ontolutils` version is v0.15.0

## v1.4.0.0

- update to newer version of the ontology
- restrict ontolutils dependency to version >0.14.1 and <1.0.0
- bugfixes parsing the standard name table
- add streamlit app to semantically enrich hdf5 files