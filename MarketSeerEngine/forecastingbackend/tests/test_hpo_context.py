from django.test import SimpleTestCase
from forecastingbackend.HPOAlgorithms.HPOStrategy.BayesianHPO import BayesianHPO
from forecastingbackend.HPOAlgorithms.HPOContext.HPOContext import HPOContext
class TestHpoContext(SimpleTestCase):

	def test_setting_hpo_algorithm(self):
		bayes = BayesianHPO()
		hpo_context = HPOContext(bayes)
		self.assertEquals(type(hpo_context.hpo_algorithm.parameter_dict), dict)

	def test_getting_tuned_parameters(self):
		bayes = BayesianHPO()
		hpo_context = HPOContext(bayes)
		self.assertEquals(type(hpo_context.get_tuned_parameters()), dict)