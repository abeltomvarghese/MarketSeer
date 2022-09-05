from django.test import SimpleTestCase
from forecastingbackend.MLModels.ModelConcreteBuilders.KNNBuilder import KNNBuilder
from forecastingbackend.MLModels.ModelDirector.MLModelDirector import MLModelDirector
from sklearn.neighbors import KNeighborsRegressor

class TestMLModelDirector(SimpleTestCase):
	def test_returns_right_builder(self):
		knn_builder = KNNBuilder()
		director = MLModelDirector()
		director.builder = knn_builder
		self.assertEquals(director.builder, knn_builder)

	def test_returns_base_model(self):
		knn_builder = KNNBuilder()
		director = MLModelDirector()
		director.builder = knn_builder
		knn_model = director.build_base_model()
		self.assertEquals(type(knn_model), KNeighborsRegressor.__class__)

	def test_returns_full_model(self):
		knn_builder = KNNBuilder()
		director = MLModelDirector()
		director.builder = knn_builder
		knn_model = director.build_full_model({'leaf_size': 10, 'p': 5, 'n_neighbors': 20})
		self.assertEquals(type(knn_model), KNeighborsRegressor.__class__)