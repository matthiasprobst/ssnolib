from typing import Optional

from ontolutils import Thing, namespaces, urirefs
from pydantic import Field


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
    note: Optional[str] = Field(default=None)
    scopeNote: Optional[str] = Field(default=None, alias="scope_note")
    editorialNote: Optional[str] = Field(default=None, alias="editorial_note")
    changeNote: Optional[str] = Field(default=None, alias="change_note")
    example: Optional[str] = Field(default=None)
