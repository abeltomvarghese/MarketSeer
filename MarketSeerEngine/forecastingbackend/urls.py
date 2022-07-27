
from django.urls import path, include
from .views import StockForecastingView


urlpatterns = [
	path('api-auth', include('rest_framework.urls')),
	path('<str:stock_symbol>', StockForecastingView.as_view(), name='stockforecast'),
]
