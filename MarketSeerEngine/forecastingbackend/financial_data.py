import json
import requests
from forecastingbackend.models import WeeklyTimeseriesUnadjusted, Stock
from forecastingbackend.global_data import get_stock_info_data

def get_alpha_vantage_data(stock_ticker):
	url_string = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock_ticker}&outputsize=full&apikey=QJAFOYP3IJR5UZ00'
	json_data = requests.get(url_string).json()
	json_timeseries_data = json_data["Weekly Adjusted Time Series"]

	timeseries_list = []
	for eachday in json_timeseries_data:
		timeseries_list.append((eachday, json_timeseries_data[eachday]))

	return timeseries_list

def get_dumbstockapi_data():
	return get_stock_info_data()

def save_stock_data(stock_ticker):
	timeseries_list = get_alpha_vantage_data(stock_ticker)
	stock_dict = get_dumbstockapi_data()

	WeeklyTimeseriesUnadjusted.objects.bulk_create([
		WeeklyTimeseriesUnadjusted(
			weekly_symbol= stock_ticker,
			stock_open= cur_obj[1]['1. open'],
			stock_high= cur_obj[1]['2. high'],
			stock_low= cur_obj[1]['3. low'],
			stock_close= cur_obj[1]['4. close'],
			stock_adj_close= cur_obj[1]['5. adjusted close'],
			stock_volume=cur_obj[1]['6. volume'],
			dividend_amount=cur_obj[1]['7. dividend amount'],
			cobdate_partition= cur_obj[0]
		) for cur_obj in timeseries_list])

	Stock.objects.create(symbol=stock_ticker, name=stock_dict[stock_ticker])