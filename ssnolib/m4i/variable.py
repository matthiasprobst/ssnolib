from typing import Optional, Union

from ontolutils import namespaces, urirefs
from ontolutils.ex.m4i import NumericalVariable as M4iNumericalVariable
from ontolutils.typing import ResourceType
from pydantic import Field

from ssnolib.ssno import StandardName


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(NumericalVariable='m4i:NumericalVariable',
         hasStandardName='ssno:hasStandardName')
class NumericalVariable(M4iNumericalVariable):
    hasStandardName: Optional[Union[ResourceType, StandardName]] = Field(alias="has_standard_name", default=None)
