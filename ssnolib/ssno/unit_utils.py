import re
from typing import Union

import pint
import rdflib
from ontolutils.utils.qudt_units import qudt_lookup

_UREG = pint.UnitRegistry()


def _get_ureg():
    return _UREG


def reverse_qudt_lookup(qudt_unit: Union[str, rdflib.URIRef]):
    for k, v in qudt_lookup.items():
        if str(v) == str(qudt_unit):
            return k


def _replace_number_following_letter(text) -> str:
    """Fixes units that are formatted something like m3 and turns it into m**3"""
    # Use regex to find letters followed by numbers
    return re.sub(r'([a-zA-Z])(-?\d+)', r'\1**\2', text)


def _parse_unit(u: str) -> pint.Unit:
    return _get_ureg()(_replace_number_following_letter(u)).u


def _format_unit(q: Union[str, pint.Quantity]) -> str:
    if isinstance(q, str):
        q = _get_ureg()(q)
    return "{:~}".format(q.to_base_units().units).replace(" ", "")
