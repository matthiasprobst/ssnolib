from typing import Union, Optional

from ontolutils import namespaces, urirefs
from ontolutils.ex.schema import Project as BaseProject
from ontolutils.typing import ResourceType
from pydantic import Field

from ssnolib import StandardNameTable


@namespaces(schema="https://schema.org/",
            ssno="https://matthiasprobst.github.io/ssno#")
@urirefs(Project='schema:Project',
         usesStandardnameTable='ssno:usesStandardnameTable'
         )
class Project(BaseProject):
    """Implementation of schema:Project"""
    usesStandardnameTable: Optional[Union[StandardNameTable, ResourceType]] = Field(default=None)


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
        return f"{self.__class__.__name__}({self.identifier})"
