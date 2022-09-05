from forecastingbackend.MLModels.ModelConcreteBuilders.base_model_generator import get_base_models, get_full_model
from django.test import SimpleTestCase
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
class TestBaseModelGenerator(SimpleTestCase):

	def test_get_base_models_ds_type(self):
		model_dict = get_base_models()
		self.assertEquals(type(model_dict), dict)

	def test_get_full_mlp_model(self):
		mlp_model = get_full_model('MLP', {'hidden_layer_size': [1,2,3,4,5], 'activation': 0.5, 'solver': 0.5, 'learning_rate': 0.5})
		self.assertEquals(type(mlp_model), MLPRegressor.__class__)

	def test_get_full_knn_model(self):
		knn_model = get_full_model('KNN', {'leaf_size': 40, 'p': 0.5, 'n_neighbours': 5})
		self.assertEquals(type(knn_model), KNeighborsRegressor.__class__)