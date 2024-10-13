from ._version import __version__
from .namespace import SSNO
from .prov import Person, Organization
from .standard_name import StandardName, ScalarStandardName, VectorStandardName
from .standard_name_table import StandardNameTable, Qualification, VectorQualification, Transformation, Character, parse_table
from .prov.attribution import Attribution
from .utils import get_cache_dir
from .m4i import TextVariable

CACHE_DIR = get_cache_dir()
CONTEXT = "https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld"
__all__ = ('__version__',
           'SSNO',
           'StandardNameTable',
           'Qualification',
           'VectorQualification',
           'Transformation',
           'Attribution',
           'StandardName',
           'Character',
           'Person',
           'Organization',
           'TextVariable',
           'CONTEXT'
           )
