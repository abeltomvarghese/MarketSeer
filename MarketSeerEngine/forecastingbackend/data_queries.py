from forecastingbackend.models import DailyTimeseriesUnadjusted, Stock
from forecastingbackend.financial_data import save_stock_data
from forecastingbackend.global_data import get_stock_info_data

def ingest_alphavantage_data(stock_ticker):
	save_stock_data(stock_ticker)


def check_stock_exists_database(stock_ticker):
	processing_dict = {None : ingest_alphavantage_data}
	return_message = None
	try:
		stock_dict = get_stock_info_data()
		company_name = stock_dict[stock_ticker]
		stock_result = Stock.objects.filter(symbol=stock_ticker).first()
		processing_dict.get(stock_result, lambda x: x)(stock_ticker)
		return_message = 'stock saved'
	except KeyError:
		return_message = 'invalid stock'

	return return_message


def get_stock_data(stock_ticker):
	return DailyTimeseriesUnadjusted.objects.filter(daily_symbol=stock_ticker).order_by('cobdate_partition')