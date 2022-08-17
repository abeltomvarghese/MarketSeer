from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from forecastingbackend.data_queries import check_stock_exists_database
from forecastingbackend.forecasting_engine import get_forecast_data

import json

class StockForecastingView(APIView):
	def get(self, request, stock_symbol,ml_model, *args, **kwargs, ):

		message_prompt = check_stock_exists_database(stock_symbol)
		forecasted_data_dict = get_forecast_data(stock_symbol, ml_model) if message_prompt == 'stock saved' else None


		forecasted_json = json.dumps(forecasted_data_dict, indent=4)
		forecasted_json = json.loads(forecasted_json)
		print(forecasted_json)

		return Response(forecasted_json)










# Create your views here.
def index(request):
	return HttpResponse("This is my first response again")