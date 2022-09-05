from django.test import SimpleTestCase
from django.urls import reverse, resolve
from forecastingbackend.views import StockForecastingView

class TestUrls(SimpleTestCase):

	def test_stock_url_is_resolved(self):
		url = reverse('stockforecast', kwargs={'stock_sygmbol': 'HMC', 'ml_model': 'KNN'})
		self.assertEquals(resolve(url).func.view_class, StockForecastingView)
