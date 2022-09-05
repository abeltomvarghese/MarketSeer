from django.test import SimpleTestCase
from forecastingbackend.HPOAlgorithms.HPOStrategy.GridSearchHPO import GridSearchHPO


class TestGridSearchHPO(SimpleTestCase):

	def test_get_parameters_to_tune(self):
		grid = GridSearchHPO()
		self.assertEquals(type(grid.get_parameters_to_tune()), list)

	def test_getting_tuned_parameters(self):
		grid = GridSearchHPO()
		self.assertEquals(type(grid.get_tuned_parameters()), dict)