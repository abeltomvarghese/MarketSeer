from django.test import SimpleTestCase
from forecastingbackend.MLModels.ModelConcreteBuilders.KNNBuilder import KNNBuilder
from sklearn.neighbors import KNeighborsRegressor

class TestKNNBuilder(SimpleTestCase):
	def test_reset_works(self):
		knn_model = KNNBuilder()
		knn_model.reset()
		self.assertEquals(type(knn_model._model), KNeighborsRegressor.__class__)

	def test_release_model_works(self):
		knn_builder = KNNBuilder()
		knn_model = knn_builder.release_model
		self.assertEquals(type(knn_model), KNeighborsRegressor.__class__)

	def test_build_model_works(self):
		knn_builder = KNNBuilder()
		knn_model = knn_builder.build_model({'leaf_size': 10, 'p': 5, 'n_neighbors': 20})
		self.assertEquals(type(knn_model), KNeighborsRegressor.__class__)
