from typing import Optional, Union

from ontolutils import Thing, namespaces, urirefs, LangString
from ontolutils.ex.pimsii import Variable as BaseVariable
from ontolutils.typing import ResourceType
from pydantic import Field

from ssnolib.ssno.standard_name import StandardName


@namespaces(pims="http://www.molmod.info/semantics/pims-ii.ttl#",
            m4i="http://w3id.org/nfdi4ing/metadata4ing#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Variable='pims:Variable',
         hasStandardName='ssno:hasStandardName'
         )
class Variable(BaseVariable):
    hasStandardName: Optional[Union[StandardName, ResourceType]] = Field(default=None, alias="has_standard_name")
