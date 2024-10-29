import pathlib
import re
import uuid
from dataclasses import dataclass
from typing import Dict, Optional, List
from typing import Union

import appdirs
import rdflib
import requests


def get_cache_dir() -> pathlib.Path:
    """Get the cache directory and create it if it does not exist"""
    cache_dir = pathlib.Path(appdirs.user_cache_dir('ssnolib'))
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)
    return cache_dir


def download_file(url,
                  dest_filename: Optional[Union[str, pathlib.Path]] = None,
                  known_hash: Optional[str] = None,
                  exist_ok: bool = False,
                  **kwargs) -> pathlib.Path:
    """Download a file from a URL and check its hash
    
    Parameter
    ---------
    url: str
        The URL of the file to download
    dest_filename: str or pathlib.Path
        The destination filename
    known_hash: str
        The expected hash of the file
    exist_ok: bool
        Whether to return an existing file. Otherwise, it is overwritten.
    **kwargs
        Additional keyword arguments passed to requests.get()
    
    Returns
    -------
    pathlib.Path
        The path to the downloaded file
    """
    if dest_filename is None:
        dest_filename = get_cache_dir() / uuid.uuid4().hex
    response = requests.get(url, stream=True, **kwargs)
    response.raise_for_status()
    if response.status_code == 200:
        content = response.content

        # Calculate the hash of the downloaded content
        if known_hash:
            import hashlib
            calculated_hash = hashlib.sha256(content).hexdigest()
            if not calculated_hash == known_hash:
                raise ValueError('File does not match the expected has')

        # Save the content to a file
        dest_filename = pathlib.Path(dest_filename)
        dest_parent = dest_filename.parent
        if not dest_parent.exists():
            dest_parent.mkdir(parents=True)

        if dest_filename.exists() and exist_ok:
            return dest_filename

        dest_filename.unlink(missing_ok=True)

        with open(dest_filename, "wb") as f:
            f.write(content)

        return dest_filename
    raise RuntimeError(f'Failed to download the file from {url}')


def gpfqcs(input_str) -> Dict[int, str]:
    """gpfqcs = get_positions_from_qualification_construction_string"""

    # Use a regex to find all words inside square brackets
    words_in_brackets = re.findall(r'\[([^\]]+)\]', input_str)

    # Split the input string into parts around "standard_name"
    parts = input_str.split("standard_name")

    # Get words before and after "standard_name"
    before_words = re.findall(r'\[([^\]]+)\]', parts[0])
    after_words = re.findall(r'\[([^\]]+)\]', parts[1])

    # Create a dictionary with positions for each word
    result = {}

    # Assign negative positions to words before "standard_name"
    for i, word in enumerate(reversed(before_words)):
        # result[word] = -(i + 1)
        result[-(i + 1)] = word

    # Assign positive positions to words after "standard_name"
    for i, word in enumerate(after_words):
        # result[word] = i + 1
        result[i + 1] = word

    return result


@dataclass
class WHERE:
    s: str
    p: str
    o: str
    return_variables: Optional[List[str]] = None
    is_optional: Optional[bool] = False

    def get_variables(self):
        if self.return_variables:
            return self.return_variables
        return_variables = []
        if self.s.startswith("?"):
            return_variables.append(self.s)
        if self.o.startswith("?"):
            return_variables.append(self.o)
        return return_variables

    def __post_init__(self):
        if self.s.startswith('http'):
            self.s = f"<{self.s}>"
        if self.p.startswith('http'):
            self.p = f"<{self.p}>"

    def __str__(self):
        if self.is_optional:
            return f"OPTIONAL {{{self.s} {self.p} {self.o}}} ."
        return f"{self.s} {self.p} {self.o} ."


@dataclass
class UNION:
    a: WHERE
    b: WHERE
    return_variables: Optional[List[str]] = None

    def get_variables(self):
        return_variables = []
        if self.a.return_variables:
            return_variables.extend(self.a.return_variables)
        if self.b.return_variables:
            return_variables.extend(self.b.return_variables)
        return return_variables

    def __str__(self):
        return f"{{ {self.a} }} UNION {{ {self.b} }}"


class SparqlQuery:
    def __init__(self, query_string, variables):
        self.query_string = query_string
        self.variables = variables

    def query(self, g: rdflib.Graph):
        results = g.query(self.query_string)
        rows = []
        for result in results:
            row = {}
            for var, res in zip(self.variables, result):
                row[var] = res
            rows.append(row)

        return rows


def build_simple_sparql_query(
        prefixes: Dict,
        wheres: List[WHERE]
) -> SparqlQuery:
    prefixes_str = "\n".join([f"PREFIX {k}: <{v}>" for k, v in prefixes.items()])
    return_variables = []
    where_strs = []
    for where in wheres:
        where_strs.append(str(where))

        if where.return_variables:
            for v in where.return_variables:
                return_variables.append(v)
        else:
            return_variables.extend(where.get_variables())

    set_of_ret_variables = set(return_variables)
    select_str = "SELECT " + ' '.join(set_of_ret_variables)
    where_str = "WHERE {" + '\n'.join(where_strs) + "\n}"
    sparql_str = f"{prefixes_str}\n{select_str}\n{where_str}"

    return SparqlQuery(sparql_str, [v[1:] for v in set_of_ret_variables])


def parse_and_exclude_none(data: Dict):
    """Excludes nones and selects .value or .n3()"""
    def _parse(value):
        if isinstance(value, rdflib.BNode):
            return value.n3()
        try:
            return value.value
        except AttributeError:
            return value
    return {k: _parse(v) for k, v in data.items() if v}
