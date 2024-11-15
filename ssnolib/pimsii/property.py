from typing import Optional

from ontolutils import namespaces, urirefs
from pydantic import Field

from ssnolib.ssno import StandardName
from .variable import Variable


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            pims="http://www.molmod.info/semantics/pims-ii.ttl#")
@urirefs(Property='pims:Property',
         hasStandardName='ssno:hasStandardName')
class Property(Variable):
    hasStandardName: Optional[StandardName] = Field(alias="has_standard_name", default=None)
