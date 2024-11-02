from typing import Union, Optional

from ontolutils import Thing, namespaces, urirefs, as_id
from pydantic import HttpUrl, field_validator, Field
from pydantic import model_validator

from ssnolib import Organization, Person, StandardNameTable
from ssnolib.dcat import Dataset


@namespaces(schema="https://schema.org/",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Project='schema:Project',
         name='schema:name',
         identifier='schema:identifier',
         funder='schema:funder',
         usesStandardnameTable='ssno:usesStandardnameTable'
         )
class Project(Thing):
    """Implementation of schema:Project"""
    name: Optional[str] = Field(default=None)
    identifier: Optional[Union[str, HttpUrl]] = Field(default=None)
    funder: Optional[Union[Person, Organization]] = Field(default=None)
    usesStandardnameTable: Optional[Union[Dataset, StandardNameTable]] = Field(default=None)

    @model_validator(mode="before")
    def _change_id(self):
        return as_id(self, "identifier")

    @field_validator('identifier', mode='before')
    @classmethod
    def _identifier(cls, identifier):
        HttpUrl(identifier)
        return str(identifier)


@namespaces(schema="https://schema.org/")
@urirefs(ResearchProject='schema:ResearchProject')
class ResearchProject(Project):
    """https://schema.org/ResearchProject"""
