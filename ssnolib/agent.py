from pydantic import EmailStr

from .core import Thing


class Agent(Thing):
    """Pydantic Model for https://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    mbox: EmailStr = None
        Email address (foaf:mbox)
    """
    mbox: EmailStr = None  # foaf:mbox

    def _repr_html_(self) -> str:
        """Returns the HTML representation of the class"""
        return f"{self.__class__.__name__}({self.mbox})"


class Organization(Agent):
    """Pydantic Model for https://www.w3.org/ns/prov#Organization

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    name: str
        Name of the organization (foaf:name)
    mbox: EmailStr = None
        Email address (foaf:mbox)
    """
    name: str  # foaf:name


class Person(Agent):
    """Pydantic Model for https://www.w3.org/ns/prov#Person

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    firstName: str = None
        First name (foaf:firstName)
    lastName: str = None
        Last name (foaf:lastName)
    mbox: EmailStr = None
        Email address (foaf:mbox)

    Extra fields are possible but not explicitly defined here.
    """
    firstName: str = None  # foaf:firstName
    lastName: str = None  # foaf:lastName

    def _repr_html_(self) -> str:
        """Returns the HTML representation of the class"""
        return f"{self.__class__.__name__}({self.firstName} {self.lastName}, {self.mbox})"
