import abc
import json
import rdflib
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Callable


def serialize_fields(obj, exclude_none: bool = True, serializer: Callable = None) -> Dict:
    """Serializes the fields of a Thing object into a json-ld dictionary (without context!)"""

    def _parse_key(k):
        return k.replace('_', ' ')

    if exclude_none:
        serialized_fields = {_parse_key(k): getattr(obj, k) for k in obj.model_fields if getattr(obj, k) is not None}
    else:
        serialized_fields = {_parse_key(k): getattr(obj, k) for k in obj.model_fields}

    # datetime
    for k, v in serialized_fields.copy().items():
        if isinstance(v, Thing):
            serialized_fields[k] = serialize_fields(v, exclude_none=exclude_none, serializer=serializer)
        elif isinstance(v, list):
            serialized_fields[k] = [serialize_fields(i, exclude_none=exclude_none, serializer=serializer) for i in v]
        elif serializer:
            serialized_fields[k] = str(serializer(k, v))
        else:
            serialized_fields[k] = str(v)
    return {"@type": f"ssno:{obj.__class__.__name__}", **serialized_fields}


class SSNOlibModel(abc.ABC, BaseModel):
    """Abstract class to be used by model classes used within SSNOlib"""

    class Config:
        """pydantic config"""
        validate_assignment = True

    def __repr__(self):
        """Returns the representation of the class, which is all none-None fields"""
        fields = ", ".join([f"{k}={v}" for k, v in self.model_dump(exclude_none=True).items()])
        return f"{self.__class__.__name__}({fields})"

    @abc.abstractmethod
    def _repr_html_(self) -> str:
        """Returns the HTML representation of the class"""


class Thing(SSNOlibModel):
    """owl:Thing"""

    class JSONLDSerializer:
        def __call__(self, key, value):
            if isinstance(value, datetime):
                return value.isoformat()
            return value

    def dump_jsonld(self, id=None, context=None, exclude_none: bool = True) -> str:
        """alias for model_dump_json()"""
        if context is None:
            from . import CONTEXT
            context = CONTEXT

        g = rdflib.Graph()
        _atemp_json_dict = serialize_fields(self,
                                            exclude_none=exclude_none,
                                            serializer=self.JSONLDSerializer())

        _qudt_unit_dict = {"K": "https://qudt.org/vocab/unit/K"}

        if id is None:
            _id = '_:'
        else:
            _id = id
        jsonld = {"@context": {"@import": context},
                  "@graph": [
                      {"@id": _id,
                       **_atemp_json_dict}
                  ]}

        g.parse(data=json.dumps(jsonld), format='json-ld')
        if context:
            return g.serialize(format='json-ld',
                               context={"@import": context},
                               indent=4)
        return g.serialize(format='json-ld', indent=4)
