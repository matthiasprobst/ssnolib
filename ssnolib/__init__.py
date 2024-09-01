from ._version import __version__
from .agent import Person, Organization
from .standard_name import StandardName
from .standard_name_table import StandardNameTable
from .utils import get_cache_dir

CACHE_DIR = get_cache_dir()
CONTEXT = "https://raw.githubusercontent.com/matthiasprobst/ssno/main/ssno_context.jsonld"
__all__ = ('__version__',
           'StandardNameTable',
           'StandardName',
           'Person',
           'Organization',
           'CONTEXT',
           )
