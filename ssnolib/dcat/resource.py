from typing import Optional, Union

from ontolutils import urirefs, namespaces
from ontolutils.ex import dcat
from ontolutils.typing import ResourceType
from pydantic import Field

from ..ssno.standard_name_table import StandardNameTable


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            ssno="https://matthiasprobst.github.io/ssno#",
            )
@urirefs(Resource='dcat:Resource',
         usesStandardNameTable='ssno:usesStandardNameTable'
         )
class Resource(dcat.Resource):
    """Pydantic implementation of dcat:Resource"""
    usesStandardNameTable: Optional[Union[StandardNameTable, ResourceType]] = Field(default=None,
                                                                                    alias="uses_standard_name_table")


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            ssno="https://matthiasprobst.github.io/ssno#", )
@urirefs(Distribution='dcat:Distribution',
         usesStandardNameTable='ssno:usesStandardNameTable'
         )
class Distribution(dcat.Distribution):
    """Implementation of dcat:Distribution    """
    usesStandardNameTable: Optional[Union[StandardNameTable, ResourceType]] = Field(default=None,
                                                                                    alias="uses_standard_name_table")


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            ssno="https://matthiasprobst.github.io/ssno#", )
@urirefs(Dataset='dcat:Dataset',
         usesStandardNameTable='ssno:usesStandardNameTable'
         )
class Dataset(dcat.Dataset):
    """Implementation of dcat:Distribution"""
    usesStandardNameTable: Optional[Union[StandardNameTable, ResourceType]] = Field(default=None,
                                                                                    alias="uses_standard_name_table")
