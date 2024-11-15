import re
import warnings
from typing import Union, List, Optional

from ontolutils import namespaces, urirefs
from ontolutils.utils.qudt_units import qudt_lookup
from pydantic import HttpUrl, field_validator, Field, ConfigDict
from pydantic import ValidationError
from pydantic_core import InitErrorDetails

from ssnolib import config
from ssnolib.dcat import Dataset
from ssnolib.skos import Concept


@namespaces(ssno="https://matthiasprobst.github.io/ssno#",
            dcat="http://www.w3.org/ns/dcat#")
@urirefs(StandardName='ssno:StandardName',
         standardName='ssno:standardName',
         unit='ssno:unit',
         description='ssno:description',
         standardNameTable='ssno:standardNameTable')
class StandardName(Concept):
    """Implementation of ssno:StandardName"""
    model_config = ConfigDict(
        populate_by_name=True,
        # Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias.
        extra="ignore",  # ignore any extra fields that are not defined in the model
    )

    standardName: str = Field(alias="standard_name")
    unit: Union[str, HttpUrl]=None
    description: Union[str, List[str]] = None  # ssno:description
    standardNameTable: Union[str, Dataset, "StandardNameTable"] = Field(default=None, alias="standard_name_table")
    alias: Optional[Union["StandardName", HttpUrl, str]] = Field(default=None)

    def __getattr__(self, item):
        for field, meta in self.model_fields.items():
            if meta.alias == item:
                return getattr(self, field)
        return super().__getattr__(item)

    def __setattr__(self, key, value):
        for field, meta in self.model_fields.items():
            if meta.alias == key:
                return setattr(self, field, value)
        return super().__setattr__(key, value)

    def __str__(self) -> str:
        if self.standardName is None:
            return ''
        return self.standardName

    @field_validator("alias", mode='before')
    @classmethod
    def _alias(cls, alias: Optional["StandardName"]) -> "StandardName":
        """Parse the alias and return the alias as StandardName."""
        if alias is None:
            return None
        if isinstance(alias, str):
            if alias.startswith('_:'):
                return str(alias)
            return HttpUrl(alias)
        elif not isinstance(alias, StandardName):
            raise TypeError(f"Expected a StandardName, got {type(alias)}")
        return alias

    @field_validator("standardNameTable", mode='before')
    @classmethod
    def _parse_standard_name_table(cls, standardNameTable: Union[Dataset, str]) -> Dataset:
        """Parse the standard_name_table and return the standard_name_table as Dataset."""
        from .standard_name_table import StandardNameTable
        if isinstance(standardNameTable, Dataset):
            return standardNameTable
        elif isinstance(standardNameTable, StandardNameTable):
            return standardNameTable
        elif isinstance(standardNameTable, str):
            assert standardNameTable.startswith('http'), f"Expected a URL, got {standardNameTable}"
            return str(HttpUrl(standardNameTable))
            # from .standard_name_table import StandardNameTable
            # return StandardNameTable(id=standardNameTable)
        raise TypeError(f"Expected a Dataset, got {type(standardNameTable)}")

    @field_validator("unit", mode='before')
    @classmethod
    def _parse_unit(cls, unit: Union[HttpUrl, str], cfg) -> str:
        """Parse the unit and return the unit as string."""
        if unit is None or unit in ('', '1', '-', 1):
            return str(qudt_lookup['dimensionless'])
        if isinstance(unit, str):
            if unit.startswith('http'):
                return str(HttpUrl(unit))
            try:
                return str(qudt_lookup[unit.strip()])
            except KeyError as e:
                if config.raise_error_on_unparsable_unit:
                    err = InitErrorDetails(
                        type="value_error",
                        loc=("unit",),
                        input=unit,
                        ctx={"error": f'your_message Unable to parse: "{unit}" of standard name '
                                      f'"{cfg.data["standardName"]}"', }
                    )
                    raise ValidationError.from_exception_data(title=cls.__name__, line_errors=[err, ])
                else:
                    warnings.warn(f'Could not parse unit: "{unit}".', UserWarning)
            return str(unit)
        return str(HttpUrl(unit))

    @field_validator("standardName", mode='before')
    @classmethod
    def _parse_standard_name(cls, standardName: str) -> str:
        """Parse the standardName and return the standardName as string."""
        if not re.match(config.standard_name_core_pattern, standardName):
            raise ValueError(f"Invalid standard name '{standardName}' according to the core pattern "
                             f"'{config.standard_name_core_pattern}'.")
        return str(standardName)


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(ScalarStandardName='ssno:ScalarStandardName')
class ScalarStandardName(StandardName):
    pass


@namespaces(ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(VectorStandardName='ssno:VectorStandardName')
class VectorStandardName(StandardName):
    pass
