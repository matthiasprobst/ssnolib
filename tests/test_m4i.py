import unittest

from ssnolib import StandardName
from ssnolib.m4i import NumericalVariable


class TestM4i(unittest.TestCase):

    def testNumericalVariableWithoutStandardName(self):
        numerical_variable = NumericalVariable(
            hasUnit='Unit',
            hasNumericalValue=1.0,
            hasMaximumValue=2.0,
            hasVariableDescription='Variable description')
        self.assertEqual(numerical_variable.hasUnit, 'Unit')
        self.assertEqual(numerical_variable.hasNumericalValue, 1.0)
        self.assertEqual(numerical_variable.hasMaximumValue, 2.0)
        self.assertEqual(numerical_variable.hasVariableDescription, 'Variable description')
        self.assertEqual(numerical_variable.hasStandardName, None)

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
        self.assertEqual(numerical_variable.hasUnit, 'mm/s')
        self.assertEqual(numerical_variable.hasNumericalValue, 1.0)
        self.assertEqual(numerical_variable.hasMaximumValue, 2.0)
        self.assertEqual(numerical_variable.hasVariableDescription, 'Variable description')
        self.assertEqual(numerical_variable.hasStandardName.standardName, 'x_velocity')
        self.assertEqual(numerical_variable.hasStandardName.unit, 'http://qudt.org/vocab/unit/M-PER-SEC')
