from typing import Union, Optional

from ontolutils import namespaces, urirefs
from pydantic import Field, HttpUrl, field_validator

from ssnolib.ssno import StandardName
from .variable import Variable


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            pims="http://www.molmod.info/semantics/pims-ii.ttl#")
@urirefs(Property='pims:Property',
         hasStandardName='ssno:hasStandardName')
class Property(Variable):
    hasStandardName: Optional[Union[StandardName, HttpUrl]] = Field(alias="has_standard_name", default=None)

    @field_validator("hasStandardName", mode='before')
    @classmethod
    def _hasStandardName(cls, hasStandardName: Union[StandardName, HttpUrl, str], cfg):
        if isinstance(hasStandardName, StandardName):
            return hasStandardName
        return str(HttpUrl(hasStandardName))
