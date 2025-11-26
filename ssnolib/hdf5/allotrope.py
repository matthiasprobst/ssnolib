from typing import Optional, Union

from ontolutils import namespaces, urirefs
from ontolutils.ex.hdf5 import Dataset as BaseHdfDataset
from ontolutils.ex.hdf5 import File as BaseHdfFile
from ontolutils.typing import ResourceType
from pydantic import Field

from .. import StandardNameTable, StandardName


@namespaces(
    ssno="https://matthiasprobst.github.io/ssno#",
    hdf5="http://purl.allotrope.org/ontologies/hdf5/1.8#"
)
@urirefs(Dataset='hdf5:Dataset',
         standardName="ssno:standardName",
         hasStandardName="ssno:hasStandardName")
class Dataset(BaseHdfDataset):
    """Dataset"""
    standardName: Optional[str] = Field(default=None, alias="standard_name")
    hasStandardName: Optional[Union[ResourceType, StandardName]] = Field(alias="has_standard_name", default=None)


@namespaces(hdf5="http://purl.allotrope.org/ontologies/hdf5/1.8#",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(File='hdf5:File',
         usesStandardNameTable='ssno:usesStandardNameTable')
class File(BaseHdfFile):
    """File"""
    usesStandardNameTable: Optional[Union[StandardNameTable, ResourceType]] = Field(default=None,
                                                                                    alias="uses_standard_name_table")
