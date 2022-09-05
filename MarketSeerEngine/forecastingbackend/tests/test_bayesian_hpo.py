from django.test import SimpleTestCase
from forecastingbackend.HPOAlgorithms.HPOStrategy.BayesianHPO import BayesianHPO


class TestBayesianHPO(SimpleTestCase):

	def test_get_parameters_to_tune(self):
		bayes = BayesianHPO()
		self.assertEquals(type(bayes.get_parameters_to_tune()), list)

	def test_getting_tuned_parameters(self):
		bayes = BayesianHPO()
		self.assertEquals(type(bayes.get_tuned_parameters()), dict)