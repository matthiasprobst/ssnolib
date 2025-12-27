import unittest

from ontolutils import serialize
from ontolutils.ex.m4i import Tool

from ssnolib import StandardName
from ssnolib.sosa import ObservableProperty
from ontolutils.ex.sosa import Sensor, Platform


class TestSosa(unittest.TestCase):

    def test_obervable_property(self):
        oprop = ObservableProperty(
            id="http://example.org/observable_property/1",
            hasStandardName=StandardName(
                standard_name="air_temperature",
                unit="https://qudt.org/vocab/unit/DEG_C"
            ),
            isObservedBy="http://example.org/sensor/1"
        )
        self.assertEqual(oprop.serialize("ttl"),
                         """@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

<http://example.org/observable_property/1> a sosa:ObservableProperty ;
    sosa:isObservedBy <http://example.org/sensor/1> ;
    ssno:hasStandardName [ a ssno:StandardName ;
            ssno:standardName "air_temperature" ;
            ssno:unit <https://qudt.org/vocab/unit/DEG_C> ] .

""")

    def test_platform(self):
        oprop = ObservableProperty(
            id="http://example.org/observable_property/1",
            hasStandardName=StandardName(
                standard_name="air_temperature",
                unit="https://qudt.org/vocab/unit/DEG_C"
            ),
            isObservedBy="http://example.org/sensor/1"
        )
        sensor = Sensor(
            id="http://example.org/sensor/1",
            observes=oprop,
            isHostedBy="http://example.org/platform/1"
        )
        platform = Platform(
            id="http://example.org/platform/1",
            hosts=sensor
        )
        print(platform.serialize("ttl"))
        self.assertEqual(platform.serialize("ttl"), """@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix ssno: <https://matthiasprobst.github.io/ssno#> .

<http://example.org/observable_property/1> a sosa:ObservableProperty ;
    sosa:isObservedBy <http://example.org/sensor/1> ;
    ssno:hasStandardName [ a ssno:StandardName ;
            ssno:standardName "air_temperature" ;
            ssno:unit <https://qudt.org/vocab/unit/DEG_C> ] .

<http://example.org/platform/1> a sosa:Platform ;
    sosa:hosts <http://example.org/sensor/1> .

<http://example.org/sensor/1> a sosa:Sensor ;
    sosa:isHostedBy <http://example.org/platform/1> ;
    sosa:observes <http://example.org/observable_property/1> .

""")

    def test_tool_and_sensor(self):
        oprop = ObservableProperty(
            id="http://example.org/observable_property/1",
            hasStandardName=StandardName(
                standard_name="air_temperature",
                unit="https://qudt.org/vocab/unit/DEG_C"
            ),
            isObservedBy="http://example.org/sensor/1"
        )
        sensor = Sensor(
            id="http://example.org/tool/1",
            observes=oprop
        )
        tool = Tool(
            id="http://example.org/tool/1"
        )
        print(serialize(
            [tool, sensor], "ttl"
        ))
