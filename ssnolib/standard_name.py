import warnings
from typing import Union

from ontolutils import namespaces, urirefs
from pydantic import HttpUrl, field_validator, Field

from ssnolib.dcat import Dataset
from ssnolib.qudt import parse_unit
from ssnolib.skos import Concept


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            dcat="http://www.w3.org/ns/dcat#")
@urirefs(StandardName='ssno:StandardName',
         canonicalUnits='ssno:canonicalUnits',
         standardName='ssno:standardName',
         description='ssno:description',
         standardNameTable='ssno:standardNameTable')
class StandardName(Concept):
    """Implementation of ssno:StandardName"""
    canonicalUnits: str = Field(default=None, alias="canonicalUnits")
    standardName: str = Field(default=None, alias="standard_name")
    description: str = None  # ssno:description
    standardNameTable: Dataset = Field(default=None, alias="standard_name_table")

    def __str__(self) -> str:
        if self.standardName is None:
            return ''
        return self.standardName

    @field_validator("standardNameTable", mode='before')
    @classmethod
    def _parse_standard_name_table(cls, standardNameTable: Union[Dataset, str]) -> Dataset:
        """Parse the standard_name_table and return the standard_name_table as Dataset."""
        if isinstance(standardNameTable, Dataset):
            return standardNameTable
        elif isinstance(standardNameTable, str):
            assert standardNameTable.startswith('http'), f"Expected a URL, got {standardNameTable}"
            from .standard_name_table import StandardNameTable
            return StandardNameTable(identifier=standardNameTable)
        raise TypeError(f"Expected a Dataset, got {type(standardNameTable)}")

    @field_validator("canonicalUnits", mode='before')
    @classmethod
    def _parse_unit(cls, canonicalUnits: Union[HttpUrl, str]) -> str:
        """Parse the canonicalUnits and return the canonicalUnits as string."""
        if canonicalUnits is None:
            return parse_unit('dimensionless')
        if isinstance(canonicalUnits, str):
            if canonicalUnits.startswith('http'):
                return str(HttpUrl(canonicalUnits))
            try:
                return str(parse_unit(canonicalUnits))
            except KeyError:
                warnings.warn(f'Could not parse canonicalUnits: "{canonicalUnits}".', UserWarning)
            return str(canonicalUnits)
        return str(HttpUrl(canonicalUnits))
