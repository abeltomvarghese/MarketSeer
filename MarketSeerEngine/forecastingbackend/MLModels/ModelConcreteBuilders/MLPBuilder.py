from __future__ import annotations
from sklearn.neural_network import MLPRegressor
from forecastingbackend.MLModels.ModelInterface.MLModelBuilder import MLModelBuilder

class MLPBuilder(MLModelBuilder):
	def __init__(self) -> None:
		self.reset()

	def reset(self) -> None:
		self._model = MLPRegressor()

	@property
	def release_model(self):
		completed_model = self._model
		self.reset()
		return completed_model


	def build_model(self, hyper_param_dict: dict):
		if hyper_param_dict is None:
			self._model = MLPRegressor()
		else:
			self._model = MLPRegressor(
				hidden_layer_sizes=hyper_param_dict["hidden_layer_sizes"],
				activation=hyper_param_dict["activation"],
				learning_rate=hyper_param_dict["learning_rate"],
				solver=hyper_param_dict["solver"]
			)
		return self.release_model