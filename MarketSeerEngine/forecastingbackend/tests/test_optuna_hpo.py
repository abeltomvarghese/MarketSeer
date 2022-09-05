from django.test import SimpleTestCase
from forecastingbackend.HPOAlgorithms.HPOStrategy.OptunaHPO import OptunaHPO


class TestRandomSearchHPO(SimpleTestCase):

	def test_get_parameters_to_tune(self):
		optuna = OptunaHPO()
		self.assertEquals(type(optuna.get_parameters_to_tune()), list)

	def test_getting_tuned_parameters(self):
		optuna = OptunaHPO()
		self.assertEquals(type(optuna.get_tuned_parameters()), dict)