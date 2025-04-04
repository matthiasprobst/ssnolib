# ssnolib: Library for the simple standard name ontology SSNO

![Tests](https://github.com/matthiasprobst/SSNOlib/actions/workflows/tests.yml/badge.svg)
![DOCS](https://codecov.io/gh/matthiasprobst/SSNOlib/branch/main/graph/badge.svg)
![pyvers](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![ssno](https://img.shields.io/badge/ssno-1.5.1-orange)

A Python library to work with the [SSNO ontology](https://matthiasprobst.github.io/ssno/1.5.1). It provides Python classes
for the ontology classes and facilitates the creation of JSON-LD files. JSON-LD files are both human- and machine-readable 
and most importantly machine-actionable. The library can be integrated in you data (conversion) pipelines.

> **_NOTE:_** The version of the library corresponds to the version of the ontology it supports. Hence, 1.5.0.1 refers 
> to the ontology version 1.5.0 and the last part (.1) is the patch version of this library.


## Documentation
Please find the online documentation [here](https://ssnolib.readthedocs.io/en/latest/). What you will find, is 
effectively the rendered versions of the Jupyter Notebooks under `/docs/tutorials/`. 


## Quickstart

### Programmatically

With `ssnolib` you can create Standard Names and their tables quickly and easily. You can find Jupyter Lab Notebooks
explaining working with [Standard names here](docs/Standard%20Name.ipynb)
or [Standard Name Tables here](docs/StandardNameTable.ipynb).

### Graphically (locally run Web App)
There are 2 apps:

1. A `streamlit` app to semantically enrich HDF5 files. This app is available with the installation of the `hdf` extra.
2. A `flask` app to create and manage Standard Name Tables. This app is available with the installation of the `app` extra.

To install the web app, run the following command:
```bash
pip install ssnolib[app,hdf]
```

To start the GUI, run the following command:
```bash
ssnolib --h5sn
```
or
```bash
ssnolib --app
```
This will start a local development server with the default port 5000 and the local host IP: `https://127.0.0.1:5000/`
(see image below).

**Note**: The web app is work in progress! Some errors might not be caught correctly. Also, you should not expose this 
web app to the public. However, feel free to use it locally in your project. I am happy to receive feedback or 
contributions to enhance the web interface! Thanks!

<img src="./docs/Screenshot_webapp.png" width="300" />

## Example Codes

The code below gives a quick insight using the *sSNOlib* classes:

```python
import ssnolib
from ssnolib.dcat import Distribution

distribution = Distribution(
    title='XML Table',
    download_URL='https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
    media_type='application/xml'
)
snt = ssnolib.StandardNameTable(title='CF Standard Name Table (latest version)',
                                distribution=distribution)
print(snt.model_dump_jsonld())
```

The last line dumps the object to a JSON-LD string:

```json
{
    "@context": {
        "owl": "https://www.w3.org/2002/07/owl#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "dcat": "http://www.w3.org/ns/dcat#",
        "dcterms": "http://purl.org/dc/terms/",
        "prov": "http://www.w3.org/ns/prov#",
        "ssno": "https://matthiasprobst.github.io/ssno#"
    },
    "@type": "ssno:StandardNameTable",
    "@id": "_:Ncbf5f941ea5447aa9ce212a2bb8d0be2",
    "dcterms:title": "CF Standard Name Table (latest version)",
    "dcat:distribution": [
        {
            "@type": "dcat:Distribution",
            "@id": "_:Nce83c15ff61640e68ba4468ebf016787",
            "dcterms:title": "XML Table",
            "dcat:downloadURL": "https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml",
            "dcat:mediaType": "https://www.iana.org/assignments/media-types/application/xml"
        }
    ]
}
```

## Installation

```bash
pip install ssnolib
```

### Extras

To be able to work with the local web app (using flask):
    
```bash
pip install ssnolib[app]
```

To be able to read standard name tables in XML format (e.g. the cfconvetions.org standard name table), you need to add
the `xml` extra:

```bash
pip installssnolib[xml]
``` 

To be able to read standard name table from YAML files, you need to add the `yaml` extra:

```bash
pip install ssnolib[yaml]
``` 

## Documentation

A complete documentation is still under development. However, the docstrings of the classes and methods should be
sufficient to get started. Also have a look at the [Tutorial Notebook](docs/Tutorial.ipynb) or following class diagram
and the [examples](#examples) below.

## Examples

Describe a Standard Name Table, e.g. the one from cfconventions.org:

```python
import ssnolib
from ssnolib.dcat import Distribution

# Create a distribution object (downloadable XML file containing the standard name table)
distribution = Distribution(title='XML Table',
                            downloadURL='https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml',
                            mediaType='application/xml')

# Create a standard name table object
snt = ssnolib.StandardNameTable(title='CF Standard Name Table v79',
                                distribution=[distribution, ])

# To describe this standard name table, we can export the JSON-LD file:
with open('cf79.jsonld', 'w', encoding='utf-8') as f:
    f.write(snt.model_dump_jsonld())
```

The corresponding JSON-LD file looks like this (showing only 2 standard names for shortness):

```json
{
    "@context": {
        "owl": "https://www.w3.org/2002/07/owl#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "dcat": "http://www.w3.org/ns/dcat#",
        "dcterms": "http://purl.org/dc/terms/",
        "prov": "http://www.w3.org/ns/prov#",
        "ssno": "https://matthiasprobst.github.io/ssno#"
    },
    "@type": "ssno:StandardNameTable",
    "@id": "_:N82e22ada2da9427fba343d0f978e98e9",
    "dcterms:title": "CF Standard Name Table v79",
    "dcat:distribution": [
        {
            "@type": "dcat:Distribution",
            "@id": "_:N8588e715cf1e4216ba142eea6f1b297d",
            "dcterms:title": "XML Table",
            "dcat:downloadURL": "https://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml",
            "dcat:mediaType": "https://www.iana.org/assignments/media-types/application/xml"
        }
    ]
}
```

### Standard name to JSON-LD
A standard name alone can be described like this:

```python
import ssnolib

air_temp = ssnolib.StandardName(standardName='air_temperature',
                                canonicalUnits='K',
                                description='Air temperature is the bulk temperature of the air, not the surface (skin) temperature.')

# write to JSON-LD
with open('air_temperature.jsonld', 'w') as f:
    f.write(air_temp.model_dump_jsonld())
```

The corresponding JSON-LD file:

```json
{
    "@context": {
        "owl": "https://www.w3.org/2002/07/owl#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "ssno": "https://matthiasprobst.github.io/ssno#",
        "dcat": "http://www.w3.org/ns/dcat#"
    },
    "@type": "ssno:StandardName",
    "@id": "_:Naaf73045ffbe415f9ad28cc3daacd3e6",
    "ssno:canonicalUnits": "http://qudt.org/vocab/unit/K",
    "ssno:standardName": "air_temperature",
    "ssno:description": "Air temperature is the bulk temperature of the air, not the surface (skin) temperature."
}
```

## Qualifications
QUalification can modify standard names by adding phrases to existing standard names. A qualification defines valid 
phrases (valid values) to be used in front of or after a standard name. Since multiple qualifications can be defined. 
they may also lead or follow other qualifications. A qualification may also have a preposition like "at" for example. 

The class `StandardNameTable` can generate a regex pattern from the qualification definitions.

## And now?
You can now take the JSON-LD file and use it with your data (place it next to it, upload it to a server, etc.).

## Contribution

Contributions are welcome. Please open an issue or a pull request.
