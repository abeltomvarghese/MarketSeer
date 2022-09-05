
from django.urls import path, include
from .views import StockForecastingView


urlpatterns = [
	path('api-auth', include('rest_framework.urls')),
	path('<str:stock_symbol>/<str:ml_model>', StockForecastingView.as_view(), name='stockforecast'),
]
