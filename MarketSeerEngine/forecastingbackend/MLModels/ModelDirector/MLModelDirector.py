from __future__ import annotations
from forecastingbackend.MLModels.ModelInterface import MLModelBuilder
class MLModelDirector():
	def __init__(self) -> None:
		self._model_builder = None

	@property
	def builder(self) -> MLModelBuilder.MLModelBuilder:
		return self._model_builder

	@builder.setter
	def builder(self, builder: MLModelBuilder.MLModelBuilder) -> None:
		self._model_builder = builder

	def build_base_model(self):
		return self._model_builder.release_model

	def build_full_model(self, hyper_param_dict):
		self._model_builder.build_model(hyper_param_dict)
		return self._model_builder.release_model