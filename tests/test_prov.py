import pathlib

import ssnolib
import unittest
from ssnolib import prov

__this_dir__ = pathlib.Path(__file__).parent
CACHE_DIR = ssnolib.utils.get_cache_dir()


class TestPROV(unittest.TestCase):

    def test_agent(self):
        agent = prov.Agent(
            id='_:b1',
            name='Agent name',
            mbox='a@email.com')
        self.assertEqual(agent.id, '_:b1')

        agent = prov.Agent(
            id='_:b1',
            name='Agent name',
            wasRoleIn='_:b2')
        self.assertEqual(agent.id, '_:b1')
        self.assertEqual(agent.wasRoleIn, '_:b2')
