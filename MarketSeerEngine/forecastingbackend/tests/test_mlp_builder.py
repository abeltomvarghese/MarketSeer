from django.test import SimpleTestCase
from forecastingbackend.MLModels.ModelConcreteBuilders.MLPBuilder import MLPBuilder
from sklearn.neural_network import MLPRegressor


class TestMLPBuilder(SimpleTestCase):
	def test_reset_works(self):
		mlp_model = MLPBuilder()
		mlp_model.reset()
		self.assertEquals(type(mlp_model._model), MLPRegressor.__class__)

	def test_release_model_works(self):
		mlp_builder = MLPBuilder()
		mlp_model = mlp_builder.release_model
		self.assertEquals(type(mlp_model), MLPRegressor.__class__)

	def test_build_model_works(self):
		mlp_builder = MLPBuilder()
		mlp_model = mlp_builder.build_model({'hidden_layer_size': [1,2,3,4,5], 'activation': 0.5, 'solver': 0.5, 'learning_rate': 0.5})
		self.assertEquals(type(mlp_model), MLPRegressor.__class__)
