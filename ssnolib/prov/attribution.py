from typing import Union, List

from ontolutils import Thing, namespaces, urirefs, as_id
from pydantic import EmailStr, HttpUrl, Field, field_validator, model_validator
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..dcat.role import Role  # Only imported for type checking and forward reference

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
    mbox: EmailStr = Field(default=None, alias="email")  # foaf:mbox


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

    @model_validator(mode="before")
    def _change_id(self):
        return as_id(self, "hasRorId")

    def to_text(self) -> str:
        """Return the text representation of the class"""
        parts = [self.name]
        if self.mbox:
            parts.append(f"{self.mbox}")
        if self.url:
            parts.append(f"URL: {self.url}")
        if self.hasRorId:
            parts.append(f"ROR ID: {self.hasRorId}")
        return '; '.join(parts)


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
        ORCID ID of person (m4i:orcidId)

    Extra fields are possible but not explicitly defined here.
    """
    firstName: str = Field(default=None, alias="first_name")  # foaf:firstName
    lastName: str = Field(default=None, alias="last_name")  # foaf:last_name
    orcidId: str = Field(default=None, alias="orcid_id")  # m4i:orcidId
    affiliation: Organization = Field(default=None)  # schema:affiliation

    @model_validator(mode="before")
    def _change_id(self):
        return as_id(self, "orcidId")

    def to_text(self) -> str:
        """Return the text representation of the class"""
        parts = []
        if self.firstName and self.lastName:
            parts.append(f"{self.lastName}, {self.firstName}")
        elif self.lastName:
            parts.append(self.lastName)
        if self.mbox:
            parts.append(f"{self.mbox}")
        if self.orcidId:
            parts.append(f"ORCID: {self.orcidId}")
        if self.affiliation:
            parts.append(f"{self.affiliation.to_text()}")
        return '; '.join(parts)


@namespaces(prov="http://www.w3.org/ns/prov#",
            dcat="http://www.w3.org/ns/dcat#")
@urirefs(Attribution='prov:Attribution',
         agent='prov:agent',
         hadRole='dcat:hadRole')
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
        from ..dcat.role import Role
        if isinstance(hadRole, Role):
            return hadRole
        HttpUrl(hadRole)
        return str(hadRole)

    @field_validator('agent', mode='before')
    @classmethod
    def _agent(cls, agent):
        if isinstance(agent, dict):
            _type = str(agent.get("type", agent.get("@type", "")))
            if "Organization" in _type:
                return Organization(**agent)
            elif "Person" in _type:
                return Person(**agent)
        return agent
