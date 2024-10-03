from typing import Union, List

from ontolutils import Thing, namespaces, urirefs
from pydantic import EmailStr, HttpUrl, Field, field_validator


@namespaces(prov="http://www.w3.org/ns/prov#",
            foaf="http://xmlns.com/foaf/0.1/")
@urirefs(Agent='prov:Agent',
         mbox='foaf:mbox')
class Agent(Thing):
    """Pydantic Model for http://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    mbox: EmailStr = None
        Email address (foaf:mbox)
    """
    mbox: EmailStr = None  # foaf:mbox

    # def _repr_html_(self) -> str:
    #     """Returns the HTML representation of the class"""
    #     return f"{self.__class__.__name__}({self.mbox})"


@namespaces(schema='https://schema.org/',
            foaf='http://xmlns.com/foaf/0.1/',
            m4i='http://w3id.org/nfdi4ing/metadata4ing#',
            prov='http://www.w3.org/ns/prov#')
@urirefs(Organization='prov:Organization',
         name='foaf:name',
         url='schema:url',
         hasRorId='m4i:hasRorId')
class Organization(Agent):
    """Pydantic Model for http://www.w3.org/ns/prov#Organization

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    name: str
        Name of the Organization (foaf:name)
    url: HttpUrl = None
        URL of the item. From schema:url.
    hasRorId: HttpUrl
        A Research Organization Registry identifier, that points to a research organization
    """
    name: str  # foaf:name
    url: Union[str, HttpUrl] = None
    hasRorId: Union[str, HttpUrl] = Field(alias="ror_id", default=None)


@namespaces(prov="http://www.w3.org/ns/prov#",
            foaf="http://xmlns.com/foaf/0.1/",
            m4i='http://w3id.org/nfdi4ing/metadata4ing#',
            schema="https://schema.org/")
@urirefs(Person='prov:Person',
         firstName='foaf:firstName',
         lastName='foaf:lastName',
         orcidId='m4i:orcidId',
         affiliation='schema:affiliation')
class Person(Agent):
    """Pydantic Model for http://www.w3.org/ns/prov#Person

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    firstName: str = None
        First name (foaf:firstName)
    lastName: str = None
        Last name (foaf:lastName)
    orcidId: str = None
        ORCID ID of person (m4i:orcidID)
    hadRole: HttpUrl
        prov:hadRole references the Role (i.e. the function of an entity with respect to an activity)
    wasRoleIn: HttpUrl
        prov:wasRoleIn references the association (e.g. between an agent and an activity) in which a role shall be defined. Inverse property of prov:hadRole.

    Extra fields are possible but not explicitly defined here.
    """
    firstName: str = Field(default=None, alias="first_name")  # foaf:firstName
    lastName: str = Field(default=None, alias="last_name")  # foaf:last_name
    orcidId: str = Field(default=None, alias="orcid_id")  # m4i:orcidID
    affiliation: Organization = Field(default=None, alias="affiliation")  # schema:affiliation


@namespaces(prov="http://www.w3.org/ns/prov#")
@urirefs(Role='prov:Role')
class Role(Thing):
    """prov:Role"""


@namespaces(prov="http://www.w3.org/ns/prov#")
@urirefs(Attribution='prov:Attribution',
         agent='prov:agent',
         hadRole='prov:hadRole')
class Attribution(Thing):
    """Pydantic Model for http://www.w3.org/ns/prov#Agent

    .. note::

        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    agent: Agent
        Person or Organization
    hadRole: Role
        Role of the agent
    """
    agent: Union[Person, List[Person], Organization, List[Organization], List[Union[Person, Organization]]]
    hadRole: Union[str, HttpUrl] = Field(alias="had_role", default=None)

    @field_validator('hadRole', mode='before')
    @classmethod
    def _hadRole(cls, hadRole: HttpUrl):
        HttpUrl(hadRole)
        return str(hadRole)
