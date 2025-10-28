from typing import Optional, Union, List, Tuple, Any

from ontolutils import Thing, namespaces, urirefs
from ontolutils.typing import ResourceType
from pydantic import Field, field_validator
from pydantic.functional_validators import WrapValidator
from typing_extensions import Annotated

from .. import StandardNameTable, StandardName
from ..dcat import Dataset as DcatDataset


def is_internal_hdf5_path(path: str, handler):
    if not path.startswith('/'):
        raise ValueError("HDF5 path must start with '/'")
    return path


def is_hdf5_root_path(path: str, handler):
    if path != '/':
        raise ValueError("HDF5 root path must be '/'")
    return path


HDF5Path = Annotated[str, WrapValidator(is_internal_hdf5_path)]
HDF5RootPath = Annotated[str, WrapValidator(is_internal_hdf5_path)]


@namespaces(
    ssno="https://matthiasprobst.github.io/ssno#",
    hdf5="http://purl.allotrope.org/ontologies/hdf5/1.8#"
)
@urirefs(Dataset='hdf5:Dataset',
         name='hdf5:name',
         standardName="ssno:standardName",
         hasStandardName="ssno:hasStandardName")
class Dataset(Thing):
    """Dataset"""
    name: HDF5Path
    standardName: Optional[str] = Field(default=None, alias="standard_name")
    hasStandardName: Optional[Union[ResourceType, StandardName]] = Field(alias="has_standard_name", default=None)


@namespaces(hdf5="http://purl.allotrope.org/ontologies/hdf5/1.8#")
@urirefs(Group='hdf5:Group',
         member='hdf5:member',
         name='hdf5:name')
class Group(Thing):
    """hdf5:Group"""
    name: HDF5Path
    member: Any = Field(default=None)

    @field_validator("member", mode="before")
    @classmethod
    def check_member(cls, group_or_dataset):
        if isinstance(group_or_dataset, (List, Tuple)):
            for item in group_or_dataset:
                if not isinstance(item, (Group, Dataset)):
                    raise ValueError("Group member must be of type GroupOrDataset")
            return group_or_dataset
        if not isinstance(group_or_dataset, (Group, Dataset)):
            raise ValueError("Group member must be of type GroupOrDataset")
        return group_or_dataset


@namespaces(hdf5="http://purl.allotrope.org/ontologies/hdf5/1.8#",
            m4i="https://matthiasprobst.github.io/ssno#")
@urirefs(File='hdf5:File',
         rootGroup='hdf5:rootGroup',
         usesStandardNameTable='hdf5:usesStandardNameTable')
class File(Thing):
    """Dataset"""
    rootGroup: Optional[Group] = Field(default=None, alias="root_group")
    usesStandardNameTable: Optional[Union[StandardNameTable, DcatDataset]] = Field(default=None,
                                                                                   alias="uses_standard_name_table")

    @field_validator("rootGroup", mode="before")
    @classmethod
    def _rootGroup(cls, root_group):
        if root_group.name != '/':
            raise ValueError("rootGroup must be of type Group")
        return root_group
