import requests

stock_info_dict = {}

def ingest_stock_info_data():
	global stock_info_dict

	r = requests.get("https://dumbstockapi.com/stock?exchanges=NYSE&exchanges=NASDAQ&exchanges=AMEX")
	json_data = r.json()

	for item in json_data:
		stock_info_dict[item["ticker"]] = item["name"]

def get_stock_info_data():
	if stock_info_dict is None:
		raise Exception("Dumb Stock Data not loaded")
	return stock_info_dict