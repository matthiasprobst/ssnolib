import pathlib
from typing import Union

import yaml

from ssnolib import StandardName


def read_standard_names_from_yaml(yaml_filename: Union[str, pathlib.Path]):
    yaml_filename = pathlib.Path(yaml_filename)
    if not yaml_filename.exists():
        raise FileNotFoundError(f"File {yaml_filename} does not exist")

    with open(yaml_filename, 'r') as f:
        data = yaml.safe_load(f)

    standard_names = []
    for k, v in data.items():
        standard_names.append(StandardName(standard_name=k, **v))

    return standard_names
