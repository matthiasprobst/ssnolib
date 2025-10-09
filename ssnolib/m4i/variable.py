import warnings
from typing import Optional, Union, List

from ontolutils import namespaces, urirefs, parse_unit, LangString
from pydantic import Field, field_validator

from ssnolib.pimsii import Variable
from ssnolib.ssno import StandardName


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#")
@urirefs(TextVariable='m4i:TextVariable',
         hasStringValue='m4i:hasStringValue')
class TextVariable(Variable):
    """Pydantic Model for http://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    hasStringValue: str
        String value
    """
    hasStringValue: Optional[LangString] = Field(alias="has_string_value", default=None)


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(NumericalVariable='m4i:NumericalVariable',
         hasUnit='m4i:hasUnit',
         hasNumericalValue='m4i:hasNumericalValue',
         hasMaximumValue='m4i:hasMaximumValue',
         hasStandardName='ssno:hasStandardName')
class NumericalVariable(Variable):
    hasUnit: Optional[str] = Field(alias="has_unit", default=None)
    hasNumericalValue: Optional[Union[float, List[float]]] = Field(alias="has_numerical_value", default=None)
    hasMaximumValue: Optional[float] = Field(alias="has_maximum_value", default=None)
    hasStandardName: Optional[StandardName] = Field(alias="has_standard_name", default=None)

    @field_validator("hasUnit", mode='before')
    @classmethod
    def _parse_unit(cls, unit):
        if unit.startswith("http"):
            return str(unit)
        try:
            return parse_unit(unit)
        except KeyError as e:
            warnings.warn(f"Unit '{unit}' could not be parsed to QUDT IRI. This is a process based on a dictionary "
                          f"lookup. Either the unit is wrong or it is not yet included in the dictionary. ")
        return str(unit)
