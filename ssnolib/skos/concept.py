from typing import Optional, List, Union

from ontolutils import Thing, namespaces, urirefs
from pydantic import field_validator, Field


@namespaces(skos="http://www.w3.org/2004/02/skos/core#",
            dcterms="http://purl.org/dc/terms/",
            prov="http://www.w3.org/ns/prov#")
@urirefs(Note='skos:Note',
         value='rdf:value',
         created='dcterms:created',
         wasRevisionOf='prov:wasRevisionOf',
         creator='dcterms:creator')
class Note(Thing):
    value: str = Field(alias="rdf_value")
    created: Optional[str] = Field(default=None)
    wasRevisionOf: Optional[Thing] = Field(default=None, alias="wasRevisionOf")
    creator: Optional[Thing] = Field(default=None)


@namespaces(skos="http://www.w3.org/2004/02/skos/core#")
@urirefs(Concept='skos:Concept',
         prefLabel='skos:prefLabel',
         altLabel='skos:altLabel',
         hiddenLabel='skos:hiddenLabel',
         definition='skos:definition',
         note='skos:note',
         scopeNote='skos:scopeNote',
         editorialNote='skos:editorialNote',
         changeNote='skos:changeNote',
         example='skos:example')
class Concept(Thing):
    """Implementation of skos:Concept"""

    prefLabel: Optional[str] = Field(default=None, alias="pref_label")
    altLabel: Optional[str] = Field(default=None, alias="alt_label")
    hiddenLabel: Optional[str] = Field(default=None, alias="hidden_label")
    definition: Optional[str] = Field(default=None)
    note: Optional[List[Union[str, Note]]] = Field(default=None)
    scopeNote: Optional[List[Union[str, Note]]] = Field(default=None, alias="scope_note")
    editorialNote: Optional[List[Union[str, Note]]] = Field(default=None, alias="editorial_note")
    changeNote: Optional[List[Union[str, Note]]] = Field(default=None, alias="change_note")
    example: Optional[str] = Field(default=None)

    @field_validator('note', mode='before')
    @classmethod
    def _note(cls, note):
        if not isinstance(note, list):
            return [note, ]
        return note

    @field_validator('scopeNote', mode='before')
    @classmethod
    def _scopeNote(cls, note):
        if not isinstance(note, list):
            return [note, ]
        return note

    @field_validator('editorialNote', mode='before')
    @classmethod
    def _editorialNote(cls, note):
        if not isinstance(note, list):
            return [note, ]
        return note

    @field_validator('changeNote', mode='before')
    @classmethod
    def _changeNote(cls, note):
        if not isinstance(note, list):
            return [note, ]
        return note
