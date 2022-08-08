from __future__ import annotations
from sklearn.neighbors import KNeighborsRegressor
from forecastingbackend.MLModels.ModelInterface import MLModelBuilder

class KNNBuilder(MLModelBuilder.MLModelBuilder):
	def __init__(self) -> None:
		self.reset()

	def reset(self) -> None:
		self._model = KNeighborsRegressor()

	@property
	def release_model(self):
		completed_model = self._model
		self.reset()
		return completed_model


	def build_model(self, hyper_param_dict: dict):
		if hyper_param_dict is None:
			self._model = KNeighborsRegressor()
		else:
			self._model = KNeighborsRegressor(
				leaf_size=hyper_param_dict["leaf_size"],
				p=hyper_param_dict["p"],
				n_neighbors=hyper_param_dict["n_neighbors"]
			)
		return self.release_model