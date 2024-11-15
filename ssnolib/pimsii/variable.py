from typing import Optional, Union

from ontolutils import Thing, namespaces, urirefs
from pydantic import Field


@namespaces(pims="http://www.molmod.info/semantics/pims-ii.ttl#",
            m4i="http://w3id.org/nfdi4ing/metadata4ing#")
@urirefs(Variable='pims:Variable',
         hasVariableDescription='m4i:hasVariableDescription',
         hasSymbol='m4i:hasSymbol',
         hasValue='m4i:hasValue',
         )
class Variable(Thing):
    hasVariableDescription: Optional[str] = Field(default=None, alias="has_variable_description")
    hasSymbol: Optional[str] = Field(default=None, alias="has_symbol")
    hasValue: Optional[Union[int, float]] = Field(default=None, alias="has_value")
