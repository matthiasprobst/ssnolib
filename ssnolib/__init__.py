from ._version import __version__
from .namespace import SSNO
from .prov import Person, Organization
from .prov.attribution import Attribution
from .ssno import StandardNameTable, Qualification, VectorQualification, Transformation, Character, AgentRole, \
    VectorStandardName, StandardName, ScalarStandardName, DomainConceptSet
from .utils import get_cache_dir
from . import schema
from .ssno.standard_name_table import parse_table

CACHE_DIR = get_cache_dir()
CONTEXT = "https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld"
__all__ = ('__version__',
           'SSNO',
           'StandardNameTable',
           'Qualification',
           'VectorQualification',
           'VectorStandardName',
           'ScalarStandardName',
           'Transformation',
           'Attribution',
           'StandardName',
           'Character',
           'Person',
           'Organization',
           'AgentRole',
           'CONTEXT',
           'parse_table'
           )
