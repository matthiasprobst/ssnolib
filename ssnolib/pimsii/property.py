from typing import Union, Optional

from ontolutils import namespaces, urirefs
from ontolutils.typing import ResourceType
from pydantic import Field, HttpUrl, field_validator
from ssnolib.ssno import StandardName
from .variable import Variable


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            pims="http://www.molmod.info/semantics/pims-ii.ttl#")
@urirefs(Property='pims:Property',
         hasStandardName='ssno:hasStandardName')
class Property(Variable):
    hasStandardName: Optional[Union[StandardName, ResourceType]] = Field(alias="has_standard_name", default=None)
