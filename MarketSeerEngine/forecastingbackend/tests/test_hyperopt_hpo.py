from django.test import SimpleTestCase
from forecastingbackend.HPOAlgorithms.HPOStrategy.HyperoptHPO import HyperoptHPO


class TestRandomSearchHPO(SimpleTestCase):

	def test_get_parameters_to_tune(self):
		hyper = HyperoptHPO()
		self.assertEquals(type(hyper.get_parameters_to_tune()), list)

	def test_getting_tuned_parameters(self):
		hyper = HyperoptHPO()
		self.assertEquals(type(hyper.get_tuned_parameters()), dict)