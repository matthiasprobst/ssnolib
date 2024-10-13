from typing import Optional

from ontolutils import Thing, namespaces, urirefs
from pydantic import Field


@namespaces(m4i="http://w3id.org/nfdi4ing/metadata4ing#")
@urirefs(TextVariable='m4i:TextVariable',
         hasStringValue='m4i:hasStringValue',
         hasVariableDescription='m4i:hasVariableDescription')
class TextVariable(Thing):
    """Pydantic Model for http://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    agent: Agent
        Person or Organization
    hadRole: Role
        Role of the agent
    """
    hasStringValue: Optional[str] = Field(alias="has_string_value", default=None)
    hasVariableDescription: Optional[str] = Field(alias="has_variable_description", default=None)
