import json
import requests

def get_alpha_vantage_data(stock_ticker):
	url_string = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_ticker}&outputsize=full&apikey=QJAFOYP3IJR5UZ00'
	json_data = requests.get(url_string).json()
	json_timeseries_data = json_data['Time Series (Daily)']

	timeseries_list = []
	for eachday in json_timeseries_data:
		timeseries_list.append((eachday, json_timeseries_data[eachday]))

	return timeseries_list

def get_dumbstockapi_data():
	stock_dict = {}

	r = requests.get("https://dumbstockapi.com/stock?exchanges=NYSE&exchanges=NASDAQ&exchanges=AMEX")
	json_data = r.json()

	for item in json_data:
		stock_dict[item["ticker"]] = item["name"]

	return stock_dict