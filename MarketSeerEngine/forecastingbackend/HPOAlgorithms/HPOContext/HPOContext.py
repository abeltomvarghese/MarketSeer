from __future__ import annotations


from forecastingbackend.HPOAlgorithms.HPOStrategy import HPOStrategy

class HPOContext():

	def __init__(self, strategy: HPOStrategy.HPOStrategy):
		self._strategy = strategy

	@property
	def hpo_algorithm(self) -> HPOStrategy.HPOStrategy:
		return self._strategy

	@hpo_algorithm.setter
	def hpo_algorithm(self, strategy: HPOStrategy.HPOStrategy):
		self._strategy = strategy

	def get_tuned_parameters(self, model_type, x_data, y_data) -> dict:
		return self.hpo_algorithm.get_tuned_parameters(model_type, x_data, y_data)