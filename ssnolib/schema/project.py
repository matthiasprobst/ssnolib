from typing import Union, Optional

from ontolutils import Thing, namespaces, urirefs, as_id, LangString
from ontolutils.ex.schema import Project as BaseProject
from pydantic import Field

from ssnolib import StandardNameTable
from ssnolib.dcat import Dataset


@namespaces(schema="https://schema.org/",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Project='schema:Project',
         usesStandardnameTable='ssno:usesStandardnameTable'
         )
class Project(BaseProject):
    """Implementation of schema:Project"""
    usesStandardnameTable: Optional[Union[Dataset, StandardNameTable]] = Field(default=None)


@urirefs(ResearchProject='schema:ResearchProject')
class ResearchProject(Project):
    """Pydantic Model for schema:ResearchProject

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    tbd
    """

    def _repr_html_(self) -> str:
        """Returns the HTML representation of the class"""
        return f"{self.__class__.__name__}({self.mbox})"
