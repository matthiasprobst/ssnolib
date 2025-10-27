"""Implementation of classes
- dcat:Resource
- dcat:Distribution
- dcat:Dataset
"""
import pathlib
import re
import shutil
from datetime import datetime
from typing import Union, List, Optional

from dateutil import parser
from ontolutils import Thing, as_id, urirefs, namespaces, LangString
from ontolutils.typing import BlankNodeType
from ontolutils.typing import ResourceType
from pydantic import HttpUrl, FileUrl, field_validator, Field, model_validator

from ssnolib.utils import download_file
from .. import foaf
from .. import prov
from ..skos import Concept


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            dcterms="http://purl.org/dc/terms/", )
@urirefs(Resource='dcat:Resource',
         title='dcterms:title',
         description='dcterms:description',
         creator='dcterms:creator',
         license='dcterms:license',
         version='dcat:version',
         identifier='dcterms:identifier',
         hasPart='dcterms:hasPart')
class Resource(Thing):
    """Pydantic implementation of dcat:Resource

    .. note::

        More than the below parameters are possible but not explicitly defined here.



    Parameters
    ----------
    title: str
        Title of the resource (dcterms:title)
    description: str = None
        Description of the resource (dcterms:description)
    creator: Union[
        foaf.Agent, foaf.Organization, foaf.Person, prov.Person, prov.Agent, prov.Organization, HttpUrl,
        List[Union[foaf.Agent, foaf.Organization, foaf.Person, prov.Person, prov.Agent, prov.Organization, HttpUrl]]
    ] = None
        Creator of the resource (dcterms:creator)
    license: ResourceType = None
        License of the resource (dcat:license)
    version: str = None
        Version of the resource (dcat:version),
        best following semantic versioning (https://semver.org/lang/de/)
    identifier: str = None
        Identifier of the resource (dcterms:identifier)
    hasPart: ResourceType = None
        A related resource that is included either physically or logically in the described resource. (dcterms:hasPart)
    """
    title: Optional[Union[LangString, List[LangString]]] = None  # dcterms:title
    description: Optional[Union[LangString, List[LangString]]] = None  # dcterms:description
    creator: Union[
        foaf.Agent,
        foaf.Organization,
        foaf.Person,
        prov.Person,
        prov.Agent,
        prov.Organization,
        HttpUrl,
        BlankNodeType,
        List[
            Union[
                foaf.Agent,
                foaf.Organization,
                foaf.Person,
                prov.Person,
                prov.Agent,
                prov.Organization,
                HttpUrl,
                BlankNodeType
            ]
        ]
    ] = None  # dcterms:creator
    license: Optional[Union[ResourceType, List[ResourceType]]] = None  # dcat:license
    version: str = None  # dcat:version
    identifier: str = None  # dcterms:identifier
    hasPart: Optional[Union[ResourceType, List[ResourceType]]] = Field(default=None, alias='has_part')

    @model_validator(mode="before")
    def change_id(self):
        """Change the id to the downloadURL"""
        return as_id(self, "identifier")

    @field_validator('identifier', mode='before')
    @classmethod
    def _identifier(cls, identifier):
        """parse datetime"""
        if identifier.startswith('http'):
            return str(HttpUrl(identifier))
        return identifier


@namespaces(dcat="http://www.w3.org/ns/dcat#")
@urirefs(Distribution='dcat:Distribution',
         downloadURL='dcat:downloadURL',
         accessURL='dcat:accessURL',
         mediaType='dcat:mediaType',
         byteSize='dcat:byteSize',
         keyword='dcat:keyword')
class Distribution(Resource):
    """Implementation of dcat:Distribution

    .. note::
        More than the below parameters are possible but not explicitly defined here.


    Parameters
    ----------
    downloadURL: Union[HttpUrl, FileUrl]
        Download URL of the distribution (dcat:downloadURL)
    mediaType: ResourceType = None
        Media type of the distribution (dcat:mediaType).
        Should be defined by the [IANA Media Types registry](https://www.iana.org/assignments/media-types/media-types.xhtml)
    byteSize: int = None
        Size of the distribution in bytes (dcat:byteSize)
    keyword: List[str]
        Keywords for the distribution.
    """
    downloadURL: Union[HttpUrl, FileUrl, pathlib.Path] = Field(default=None, alias='download_URL')
    accessURL: Union[HttpUrl, FileUrl, pathlib.Path] = Field(default=None, alias='access_URL')
    mediaType: ResourceType = Field(default=None, alias='media_type')  # dcat:mediaType
    byteSize: int = Field(default=None, alias='byte_size')  # dcat:byteSize
    keyword: List[str] = None  # dcat:keyword

    def _repr_html_(self):
        """Returns the HTML representation of the class"""
        if self.downloadURL is not None:
            return f"{self.__class__.__name__}({self.downloadURL})"
        return super()._repr_html_()

    def download(self,
                 dest_filename: Union[str, pathlib.Path] = None,
                 exist_ok: bool = False,
                 **kwargs) -> pathlib.Path:
        """Downloads the distribution
        kwargs are passed to the download_file function, which goes to requests.get()"""

        if self.downloadURL is None:
            raise ValueError('The downloadURL is not defined')

        def _parse_file_url(furl):
            """in windows, we might need to strip the leading slash"""
            fname = pathlib.Path(furl)
            if fname.exists():
                return fname
            fname = pathlib.Path(self.downloadURL.path[1:])
            if fname.exists():
                return fname
            raise FileNotFoundError(f'File {self.downloadURL.path} does not exist')

        if self.downloadURL.scheme == 'file':
            if dest_filename is None:
                return _parse_file_url(self.downloadURL.path)
            else:
                return shutil.copy(_parse_file_url(self.downloadURL.path), dest_filename)
        if "#" in str(self.downloadURL):
            dest_filename = pathlib.Path(dest_filename or self.downloadURL.fragment)
        else:
            dest_filename = pathlib.Path(dest_filename or self.downloadURL.path.split('/')[-1])
        if len(dest_filename.name) <= 1:
            raise ValueError(f"Destination filename {dest_filename} is not valid")
        if dest_filename.exists():
            return dest_filename
        return download_file(
            self.downloadURL,
            dest_filename,
            exist_ok=exist_ok,
            **kwargs)

    @field_validator('mediaType', mode='before')
    @classmethod
    def _mediaType(cls, mediaType):
        """should be a valid URI, like: https://www.iana.org/assignments/media-types/text/markdown"""
        if isinstance(mediaType, str):
            if mediaType.startswith('http'):
                return HttpUrl(mediaType)
            elif mediaType.startswith('iana:'):
                return HttpUrl("https://www.iana.org/assignments/media-types/" + mediaType.split(":", 1)[-1])
            elif re.match('[a-z].*/[a-z].*', mediaType):
                return HttpUrl("https://www.iana.org/assignments/media-types/" + mediaType)
        return mediaType

    @field_validator('downloadURL', mode='before')
    @classmethod
    def _downloadURL(cls, downloadURL):
        """a pathlib.Path is also allowed but needs to be converted to a URL"""
        if isinstance(downloadURL, pathlib.Path):
            return str(FileUrl(f'file://{downloadURL.resolve().absolute()}'))
        try:
            return str(FileUrl(downloadURL))
        except ValueError:
            return str(HttpUrl(downloadURL))


@namespaces(dcat="http://www.w3.org/ns/dcat#")
@urirefs(DatasetSeries='dcat:DatasetSeries')
class DatasetSeries(Resource):
    """Pydantic implementation of dcat:DatasetSeries"""


@namespaces(dcat="http://www.w3.org/ns/dcat#",
            prov="http://www.w3.org/ns/prov#",
            dcterms="http://purl.org/dc/terms/")
@urirefs(Dataset='dcat:Dataset',
         distribution='dcat:distribution',
         modified='dcterms:modified',
         landingPage='dcat:landingPage',
         inSeries='dcat:inSeries',
         theme='dcat:theme')
class Dataset(Resource):
    """Pydantic implementation of dcat:Dataset

    .. note::

        More than the below parameters are possible but not explicitly defined here.

    Parameters
    ----------
    title: str
        Title of the resource (dcterms:title)
    description: str = None
        Description of the resource (dcterms:description)
    version: str = None
        Version of the resource (dcat:version)
    distribution: List[Distribution] = None
        Distribution of the resource (dcat:Distribution)
    landingPage: HttpUrl = None
        Landing page of the resource (dcat:landingPage)
    modified: datetime = None
        Last modified date of the resource (dcterms:modified)
    inSeries: DatasetSeries = None
        The series the dataset belongs to (dcat:inSeries)
    theme: HttpUrl or StandardNameTable = None
        A main category of the resource. A resource can have multiple themes.
    """
    # http://www.w3.org/ns/prov#Person, see https://www.w3.org/TR/vocab-dcat-3/#ex-adms-identifier
    distribution: Union[Distribution, List[Distribution]] = None  # dcat:Distribution
    modified: datetime = None  # dcterms:modified
    landingPage: HttpUrl = Field(default=None, alias='landing_page')  # dcat:landingPage
    inSeries: DatasetSeries = Field(default=None, alias='in_series')  # dcat:inSeries
    theme: Optional[Union[HttpUrl, Concept]] = Field(default=None)  # dcat:theme

    @field_validator('modified', mode='before')
    @classmethod
    def _modified(cls, modified):
        """parse datetime"""
        if isinstance(modified, str):
            return parser.parse(modified)
        return modified
