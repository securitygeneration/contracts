import unittest

from pycontracts.further import Further
from pycontracts.tests import test_forward, fresh
from pycontracts.tests.test_settings import *

class FurtherTests(
        unittest.TestCase,
        test_forward.BasicTests,
        test_forward.UseCaseTests,
        # TODO: test_forward.SecurityTests
        ):

    def deploy(self, owner):
        return Further.deploy(w3, owner, originator = faucets.random())

    def setUp(self):
        self.pk = fresh.private_key()
        self.fwd = self.deploy(address(self.pk))
