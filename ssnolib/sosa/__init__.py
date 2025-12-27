from typing import Union

from ontolutils import urirefs, namespaces
from ontolutils.ex.sosa import ObservableProperty as OntolutilsObservableProperty
from ontolutils.typing import ResourceType
from pydantic import Field

from ..ssno import StandardName


@namespaces(sosa="http://www.w3.org/ns/sosa/",
            ssno="https://matthiasprobst.github.io/ssno#"
            )
@urirefs(ObservableProperty="sosa:ObservableProperty",
         hasStandardName="ssno:hasStandardName")
class ObservableProperty(OntolutilsObservableProperty):
    """Observable Property - An observable quality (property, characteristic) of a FeatureOfInterest."""
    hasStandardName: Union[StandardName, ResourceType] = Field(default=None, alias="has_standard_name")
