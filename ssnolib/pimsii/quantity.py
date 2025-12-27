from typing import Union, Optional

from ontolutils import namespaces, urirefs
from ontolutils.typing import ResourceType
from pydantic import Field

from ssnolib.ssno import StandardName
from .variable import Variable


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            pims="http://www.molmod.info/semantics/pims-ii.ttl#")
@urirefs(QuantityValue='pims:QuantityValue',
         hasStandardName='ssno:hasStandardName')
class QuantityValue(Variable):
    hasStandardName: Optional[Union[StandardName, ResourceType]] = Field(alias="has_standard_name", default=None)
