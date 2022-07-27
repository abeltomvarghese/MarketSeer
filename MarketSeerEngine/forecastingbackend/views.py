from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from forecastingbackend.data_queries import check_stock_exists_database
from forecastingbackend.forecasting_engine import get_forecast_data

class StockForecastingView(APIView):
	def get(self, request, stock_symbol, *args, **kwargs, ):
		message_prompt = check_stock_exists_database(stock_symbol)
		if message_prompt == 'stock saved':
			forecasted_json_data = get_forecast_data(stock_symbol)



		return Response(f'The symbol passed in was a {stock_symbol}')










# Create your views here.
def index(request):
	return HttpResponse("This is my first response again")