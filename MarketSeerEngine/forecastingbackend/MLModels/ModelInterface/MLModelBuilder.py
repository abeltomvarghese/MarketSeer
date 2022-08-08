from __future__ import annotations
from abc import ABC, abstractmethod

class MLModelBuilder(ABC):

	@property
	@abstractmethod
	def release_model(self) -> None:
		pass

	@abstractmethod
	def build_model(self, hyper_param_dict: dict) -> None:
		pass