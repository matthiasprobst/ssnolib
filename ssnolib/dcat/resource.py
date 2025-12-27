from typing import Optional

from ontolutils import urirefs, namespaces
from ontolutils.ex import dcat
from ontolutils.typing import AnyIriOf
from pydantic import Field

from ..ssno.standard_name import StandardName
from ..ssno.standard_name_table import StandardNameTable


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            ssno="https://matthiasprobst.github.io/ssno#",
            )
@urirefs(Resource='dcat:Resource',
         usesStandardNameTable='ssno:usesStandardNameTable'
         )
class Resource(dcat.Resource):
    """Pydantic implementation of dcat:Resource"""
    usesStandardNameTable: Optional[AnyIriOf[StandardNameTable]] = Field(default=None,
                                                                         alias="uses_standard_name_table")


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            ssno="https://matthiasprobst.github.io/ssno#", )
@urirefs(Distribution='dcat:Distribution',
         usesStandardNameTable='ssno:usesStandardNameTable'
         )
class Distribution(dcat.Distribution):
    """Implementation of dcat:Distribution    """
    usesStandardNameTable: Optional[AnyIriOf[StandardNameTable]] = Field(default=None,
                                                                         alias="uses_standard_name_table")


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            ssno="https://matthiasprobst.github.io/ssno#", )
@urirefs(Dataset='dcat:Dataset',
         usesStandardNameTable='ssno:usesStandardNameTable',
         hasStandardName='ssno:hasStandardName'
         )
class Dataset(dcat.Dataset):
    """Implementation of dcat:Distribution"""
    usesStandardNameTable: Optional[AnyIriOf[StandardNameTable]] = Field(default=None,
                                                                         alias="uses_standard_name_table")
    hasStandardName: Optional[AnyIriOf[StandardName]] = Field(default=None, alias="has_standard_name")
