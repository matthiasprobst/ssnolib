import unittest

import pydantic

from ssnolib import StandardName
from ssnolib.m4i import NumericalVariable, Tool
from ontolutils.ex.m4i import TextVariable

class TestM4i(unittest.TestCase):

    def testNumericalVariableWithoutStandardName(self):
        with self.assertRaises(pydantic.ValidationError):
            numerical_variable = NumericalVariable(
                hasUnit='Unit',
                hasNumericalValue=1.0,
                hasMaximumValue=2.0,
                hasVariableDescription='Variable description')

    def testNumericalVariableWithStandardName(self):
        numerical_variable = NumericalVariable(
            hasUnit='mm/s',
            hasNumericalValue=1.0,
            hasMaximumValue=2.0,
            hasVariableDescription='Variable description',
            hasStandardName=StandardName(
                standardName='x_velocity',
                unit='m/s')
        )
        self.assertEqual(numerical_variable.hasUnit, 'http://qudt.org/vocab/unit/MilliM-PER-SEC')
        self.assertEqual(numerical_variable.hasNumericalValue, 1.0)
        self.assertEqual(numerical_variable.hasMaximumValue, 2.0)
        self.assertEqual(numerical_variable.hasVariableDescription, 'Variable description')
        self.assertEqual(numerical_variable.hasStandardName.standardName, 'x_velocity')
        self.assertEqual(numerical_variable.hasStandardName.unit, 'http://qudt.org/vocab/unit/M-PER-SEC')

    def test_to_xarray(self):
        numerical_variable = NumericalVariable(
            hasUnit='mm/s',
            hasNumericalValue=[1.0, 2.0, 3.0],
            hasMaximumValue=3.0,
            hasStandardName=StandardName(standard_name="x_velocity", unit="m/s"),
            hasVariableDescription='Variable description')
        xarray_data = numerical_variable.to_xarray()
        self.assertEqual(xarray_data.values.tolist(), [1.0, 2.0, 3.0])
        print(xarray_data)

        nv_from_xarray = NumericalVariable.from_xarray(xarray_data)
        self.assertEqual(nv_from_xarray.hasNumericalValue.tolist(), [1.0, 2.0, 3.0])
        self.assertEqual(nv_from_xarray.hasUnit, 'http://qudt.org/vocab/unit/MilliM-PER-SEC')
        self.assertEqual(nv_from_xarray.hasStandardName.standardName, "x_velocity")
        self.assertEqual(nv_from_xarray.hasStandardName.unit, 'http://qudt.org/vocab/unit/M-PER-SEC')
        self.assertEqual(nv_from_xarray.hasMaximumValue, 3.0)

    def test_tool(self):
        nv = NumericalVariable(
            hasUnit='mm/s',
            hasNumericalValue=1.0,
            hasMaximumValue=2.0,
            hasVariableDescription='Variable description',
            hasStandardName=StandardName(
                standardName='x_velocity',
                unit='m/s')
        )
        tv = TextVariable(
            hasTextValue='Sample text',
            hasVariableDescription='Text variable description'
        )
        tool = Tool(
            hasToolName='Test Tool',
            hasParameter=nv
        )
        self.assertEqual(tool.hasToolName, 'Test Tool')
        self.assertIsInstance(tool.hasParameter, NumericalVariable)
        self.assertEqual(tool.hasParameter.hasStandardName.standardName, 'x_velocity')

        tool_and_tv = Tool(
            hasToolName='Test Tool with TextVariable',
            hasParameter=[nv, tv, "https://example.org/variable/123"]
        )
        self.assertEqual(tool_and_tv.hasToolName, 'Test Tool with TextVariable')
        self.assertIsInstance(tool_and_tv.hasParameter, list)
        self.assertIsInstance(tool_and_tv.hasParameter[0], NumericalVariable)
        self.assertIsInstance(tool_and_tv.hasParameter[1], TextVariable)
        self.assertIsInstance(tool_and_tv.hasParameter[2], str)
        self.assertEqual(tool_and_tv.hasParameter[2], "https://example.org/variable/123")

        # invalid tool:
        invalid_tool = Tool(
            hasToolName='Test Tool',
            hasParameter=tool
        )