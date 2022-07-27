import json
import requests
from forecastingbackend.models import DailyTimeseriesUnadjusted, Stock
from forecastingbackend.global_data import get_stock_info_data

def get_alpha_vantage_data(stock_ticker):
	url_string = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_ticker}&outputsize=full&apikey=QJAFOYP3IJR5UZ00'
	json_data = requests.get(url_string).json()
	json_timeseries_data = json_data["Time Series (Daily)"]

	timeseries_list = []
	for eachday in json_timeseries_data:
		timeseries_list.append((eachday, json_timeseries_data[eachday]))

	return timeseries_list

def get_dumbstockapi_data():
	return get_stock_info_data()

def save_stock_data(stock_ticker):
	timeseries_list = get_alpha_vantage_data(stock_ticker)
	stock_dict = get_dumbstockapi_data()

	DailyTimeseriesUnadjusted.objects.bulk_create([
		DailyTimeseriesUnadjusted(
			daily_symbol= stock_ticker,
			stock_open= cur_obj[1]['1. open'],
			stock_high= cur_obj[1]['2. high'],
			stock_low= cur_obj[1]['3. low'],
			stock_close= cur_obj[1]['4. close'],
			stock_volume= cur_obj[1]['5. volume'],
			cobdate_partition= cur_obj[0]
		) for cur_obj in timeseries_list])

	Stock.objects.create(symbol=stock_ticker, name=stock_dict[stock_ticker])