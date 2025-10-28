# ssnolib: Library for the Simple Standard Name Ontology (SSNO)

![Tests](https://github.com/matthiasprobst/SSNOlib/actions/workflows/tests.yml/badge.svg)
![Coverage](https://codecov.io/gh/matthiasprobst/SSNOlib/branch/main/graph/badge.svg)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![SSNO Version](https://img.shields.io/badge/ssno-2.1.0-orange)
![License](https://img.shields.io/github/license/matthiasprobst/SSNOlib)

A Python library to work with the [SSNO ontology](https://matthiasprobst.github.io/ssno/2.1.0). It provides Python classes for ontology concepts and facilitates the creation of RDF files (JSON-LD, TTL, XML). RDF files are both human- and machine-readable, and most importantly, machine-actionable. The library can be integrated into your data (conversion) pipelines.

## Features
- Python classes for all SSNO ontology concepts
- Easy creation and export of JSON-LD, TTL, and XML files
- Support for Standard Name Tables (SNT)
- Extensible for HDF5, XML, and YAML formats
- Local web apps (Streamlit, Flask) for management and enrichment
- Compatible with Python 3.8–3.12
- Comprehensive documentation and tutorials

> **Note:** The library version matches the supported ontology version. For example, 1.5.0.1 refers to ontology version 1.5.0 and patch version .1 of the library.

## Installation

Install the core library:
```bash
pip install ssnolib
```


## Quickstart

### Describe a Standard Name and dump it to Turtl
```python
import ssnolib

air_temp = ssnolib.StandardName(
    standardName='air_temperature',
    unit='K',
    description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.@en')
with open('air_temperature.jsonld', 'w') as f:
    f.write(air_temp.model_dump_ttl())
```

The serialized TTL file looks like this:
```turtle
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

[] a ssno:StandardName ;
    ssno:description "Air temperature is the bulk temperature of the air, not the surface (skin) temperature."@en ;
    ssno:standardName "air_temperature" ;
    ssno:unit <http://qudt.org/vocab/unit/K> .
```


### Describe Standard Name Tables
A Standard Name Table (SNT) defines Standard Names and exists as an RDF file 
(usually in TTL, XML, or JSON-LD format). The SNT itself is modeled by `ssnolib.StandardNameTable`. In the 
following example, we define a SNT with one Standard Name (`air_temperature`) which is stored in a `dcat:Dataset` with one `dcat:Distribution`.
The distribution points to a TTL file containing the SNT, which can be downloaded. 
```python
import ssnolib
from ssnolib.dcat import Dataset, Distribution

distribution = Distribution(
    title='TTL Table@en',
    downloadURL='https://example.org/cf-standard-name-table.ttl',
    mediaType='text/turtle'
)
snt_dataset = Dataset(
    title='CF Standard Name Table Dataset@en',
    description='The CF Standard Name Table is a controlled vocabulary for climate and forecast metadata.@en',
    distribution=distribution
)
snt = ssnolib.StandardNameTable(
    id="https://doi.org/10.5281/zenodo.12345678",
    title='CF Standard Name Table (latest version)@en',
    dataset=snt_dataset,
    created="2023-10-10",
    standardNames=[air_temp,]
)
```

The serialized version in TTL format can be obtained by:
```python
print(snt.serialize("ttl", base_uri="https://example.org#"))
```

which results in:
```turtle
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://doi.org/10.5281/zenodo.12345678> a ssno:StandardNameTable ;
    dcterms:created "2023-10-10"^^xsd:date ;
    dcterms:title "CF Standard Name Table (latest version)"@en ;
    ssno:dataset <https://example.org/#N2f15bceee1cf431688c375b242d2c61b> ;
    ssno:standardNames <https://example.org/#N5542e225237745dfa57de897543fa5c8> .

<https://example.org/#N2f15bceee1cf431688c375b242d2c61b> a dcat:Dataset ;
    dcterms:description "The CF Standard Name Table is a controlled vocabulary for climate and forecast metadata."@en ;
    dcterms:title "CF Standard Name Table Dataset"@en ;
    dcat:distribution <https://example.org/#Ncd83fad310144161b45f7c466d6fd7cc> .

<https://example.org/#N5542e225237745dfa57de897543fa5c8> a ssno:StandardName ;
    ssno:description "Air temperature is the bulk temperature of the air, not the surface (skin) temperature."@en ;
    ssno:standardName "air_temperature" ;
    ssno:unit <http://qudt.org/vocab/unit/K> .

<https://example.org/#Ncd83fad310144161b45f7c466d6fd7cc> a dcat:Distribution ;
    dcterms:title "TTL Table"@en ;
    dcat:downloadURL <https://example.org/cf-standard-name-table.ttl> ;
    dcat:mediaType <https://www.iana.org/assignments/media-types/text/turtle> .
```

### Web App Usage

Two simple web-apps exist to manage Standard Name Tables and to semantically enrich HDF5 files with Standard Names.

1. A Streamlit app to semantically enrich HDF5 files (requires `hdf` extra)
2. A Flask app to create and manage Standard Name Tables (requires `app` extra)


Install the library with the required extras:
```bash
pip install ssnolib[app,hdf]
```


To start the GUI:
```bash
ssnolib --h5sn
```
or
```bash
ssnolib --app
```
This will start a local development server at `https://127.0.0.1:5000/`.

**Note:** The web app is work in progress. Do not expose it to the public. Feedback and contributions are welcome!

<img src="./docs/Screenshot_webapp.png" width="300" />





## Testing
To run tests:
```bash
pytest tests
```

## Contribution
Contributions are welcome! Please open an issue or pull request. Guidelines:
- Write clear commit messages
- Add tests for new features
- Document changes in CHANGELOG.md

## Citation
Please cite this project using the [CITATION.cff](./CITATION.cff).

## License
This project is licensed under the [MIT License](./LICENSE).

## Support & Contact
- Report issues: [GitHub Issues](https://github.com/matthiasprobst/SSNOlib/issues)
- Questions & feedback: [matth.probst@gmail.com](mailto:matth.probst@gmail.com)
