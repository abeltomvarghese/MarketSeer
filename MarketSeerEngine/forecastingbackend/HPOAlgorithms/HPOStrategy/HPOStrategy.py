from __future__ import annotations
from abc import ABC, abstractmethod


class HPOStrategy(ABC):

	@abstractmethod
	def get_tuned_parameters(self, model_type, x_data, y_data):
		pass

	@abstractmethod
	def get_parameters_to_tune(self, model_type):
		pass