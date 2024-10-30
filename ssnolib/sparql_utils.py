from dataclasses import dataclass
from typing import Dict, Optional, List

import rdflib


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
