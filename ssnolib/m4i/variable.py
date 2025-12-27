from typing import Optional, Union, List

from ontolutils import namespaces, urirefs
from ontolutils.ex.m4i import NumericalVariable as M4iNumericalVariable
from ontolutils.ex.m4i import TextVariable
from ontolutils.ex.m4i import Tool as M4iTool
from ontolutils.typing import ResourceType
from pydantic import Field

from ssnolib.ssno import StandardName


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(NumericalVariable='m4i:NumericalVariable',
         hasStandardName='ssno:hasStandardName')
class NumericalVariable(M4iNumericalVariable):
    hasStandardName: Optional[Union[ResourceType, StandardName]] = Field(alias="has_standard_name", default=None)

    def to_xarray(self, language: str = "en"):
        da = super().to_xarray(language=language)
        if self.hasStandardName:
            da.attrs["standard_name"] = self.hasStandardName.standardName
        return da


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Tool='m4i:Tool',
         hasParameter='ssno:hasParameter')
class Tool(M4iTool):
    # hasParameter: make_type_or_list(TextVariable, NumericalVariable) = Field(default=None, alias="parameter")
    hasParameter: Optional[Union[TextVariable, NumericalVariable, ResourceType,
    List[Union[TextVariable, NumericalVariable, ResourceType]]]] = Field(default=None, alias="parameter")
