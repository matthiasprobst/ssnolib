from typing import Optional

from ontolutils import namespaces, urirefs
from pydantic import Field

from ssnolib.ssno import StandardName
from .variable import Variable


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Property='pims-ii:Property',
         hasStandardName='ssno:hasStandardName')
class Property(Variable):
    hasStandardName: Optional[StandardName] = Field(alias="has_standard_name", default=None)
