from django.test import SimpleTestCase
from forecastingbackend.HPOAlgorithms.HPOStrategy.RandomSearchHPO import RandomSearchHPO


class TestRandomSearchHPO(SimpleTestCase):

	def test_get_parameters_to_tune(self):
		random = RandomSearchHPO()
		self.assertEquals(type(random.get_parameters_to_tune()), list)

	def test_getting_tuned_parameters(self):
		random = RandomSearchHPO()
		self.assertEquals(type(random.get_tuned_parameters()), dict)