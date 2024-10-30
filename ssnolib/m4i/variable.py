from typing import Optional

from ontolutils import namespaces, urirefs
from pydantic import Field

from ssnolib.ssno import StandardName
from ssnolib.pimsii import Variable


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#")
@urirefs(TextVariable='m4i:TextVariable',
         hasStringValue='m4i:hasStringValue',
         hasVariableDescription='m4i:hasVariableDescription')
class TextVariable(Variable):
    """Pydantic Model for http://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    hasStringValue: str
        String value
    hasVariableDescription: str
        Variable description
    """
    hasStringValue: Optional[str] = Field(alias="has_string_value", default=None)
    hasVariableDescription: Optional[str] = Field(alias="has_variable_description", default=None)


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(NumericalVariable='m4i:NumericalVariable',
         hasUnit='m4i:hasUnit',
         hasNumericalValue='m4i:hasNumericalValue',
         hasMaximumValue='m4i:hasMaximumValue',
         hasVariableDescription='m4i:hasVariableDescription',
         hasStandardName='ssno:hasStandardName')
class NumericalVariable(Variable):
    hasUnit: Optional[str] = Field(alias="has_unit", default=None)
    hasNumericalValue: Optional[float] = Field(alias="has_numerical_value", default=None)
    hasMaximumValue: Optional[float] = Field(alias="has_maximum_value", default=None)
    hasVariableDescription: Optional[str] = Field(alias="has_variable_description", default=None)
    hasStandardName: Optional[StandardName] = Field(alias="has_standard_name", default=None)
