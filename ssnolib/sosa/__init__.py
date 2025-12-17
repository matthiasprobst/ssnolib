from typing import Union, List

from ontolutils import Thing, urirefs, namespaces
from ontolutils.typing import ResourceType
from pydantic import Field
from ontolutils.ex import ssn

from ..ssno import StandardName


@namespaces(sosa="http://www.w3.org/ns/sosa/",
            ssno="https://matthiasprobst.github.io/ssno#"
            )
@urirefs(ObservableProperty="sosa:ObservableProperty",
         hasStandardName="ssno:hasStandardName")
         # isObservedBy="sosa:isObservedBy")
class ObservableProperty(ssn.ObservableProperty):
    """Observable Property - An observable quality (property, characteristic) of a FeatureOfInterest."""
    hasStandardName: Union[StandardName, ResourceType] = Field(default=None, alias="has_standard_name")
    # isObservedBy: Union[ResourceType, "Sensor", List[Union[ResourceType, "Sensor"]]] = Field(default=None, alias="is_observed_by")


# @namespaces(sosa="http://www.w3.org/ns/sosa/")
# @urirefs(Actuator="sosa:Actuator")
# class Actuator(Thing):
#     """Actuator - A device that is used by, or implements, an (Actuation) Procedure that changes the state of the world."""
#
#
# @namespaces(sosa="http://www.w3.org/ns/sosa/")
# @urirefs(Sensor="sosa:Sensor",
#          observes="sosa:observes",
#          isHostedBy="sosa:isHostedBy")
# class Sensor(Thing):
#     """Sensor -  Device, agent (including humans), or software (simulation) involved in, or implementing, a Procedure.
#     Sensors respond to a Stimulus, e.g., a change in the environment, or Input data composed from the Results of prior
#     Observations, and generate a Result. Sensors can be hosted by Platforms."""
#     observes: Union[ObservableProperty, List[ObservableProperty]]
#     isHostedBy: Union[ResourceType, "Platform", List[Union[ResourceType, "Platform"]]] = Field(
#         default=None,
#         alias="is_hosted_by",
#         description="Relation between a Sensor and a Platform that hosts or mounts it."
#     )
#
# @namespaces(sosa="http://www.w3.org/ns/sosa/")
# @urirefs(Sampler="sosa:Sampler")
# class Sampler(Thing):
#     """Sampler - A device that is used by, or implements, an (Actuation) Procedure that changes the state of the world."""
#
#
# @namespaces(sosa="http://www.w3.org/ns/sosa/")
# @urirefs(Platform="sosa:Platform",
#          hosts="sosa:hosts")
# class Platform(Thing):
#     """Platform - A Platform is an entity that hosts other entities, particularly Sensors, Actuators, Samplers, and other Platforms."""
#     hosts: Union[Actuator, Sensor, Sampler, "Platform", List[Union[Actuator, Sensor, Sampler, "Platform"]]] = Field(
#         default=None,
#         alias="hosts",
#         description="Relation between a Platform and a Sensor, Actuator, Sampler, or Platform, hosted or mounted on it."
#     )
#

# ObservableProperty.model_rebuild()
# Platform.model_rebuild()
