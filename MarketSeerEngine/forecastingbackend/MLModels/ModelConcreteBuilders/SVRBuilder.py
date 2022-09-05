from __future__ import annotations
from sklearn.svm import SVR
from forecastingbackend.MLModels.ModelInterface import MLModelBuilder

class SVRBuilder(MLModelBuilder.MLModelBuilder):

	def __init__(self) -> None:
		self.reset()

	def reset(self) -> None:
		self._model = SVR()


	@property
	def release_model(self) :
		completed_model = self._model
		self.reset()
		return completed_model

	def build_model(self, hyper_param_dict: dict):
		if hyper_param_dict is None:
			self._model = SVR()
		else:
			self._model = SVR(
				kernel=hyper_param_dict['kernel'],
				gamma=hyper_param_dict['kernel'],
				C=hyper_param_dict['C'],
				epsilon=hyper_param_dict['epsilon']
			)