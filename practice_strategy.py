import os
import alpaca_trade_api as tradeapi
import pandas as pd
import smtplib
import time
import datetime
from bs4 import BeautifulSoup
import requests
import pprint

# url stock screener 10-50: https://finance.yahoo.com/screener/unsaved/39e0a528-d7d3-48cd-9e3c-e40fc45f268c?dependentField=sector&dependentValues=
# url stock screener 10-20: https://finance.yahoo.com/screener/unsaved/a5a8fe09-189d-4314-8ff7-93ebed97d9f8
def scrape_yahoo(stock):
	five_day_data = []
	try:
		url = ('https://finance.yahoo.com/quote/' + stock + '/history?p='+stock)
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		tables = soup.findAll('table', class_='W(100%) M(0)')
		for table in tables:
			table_body = table.find('tbody')
			rows = table_body.find_all('tr')

			for row in rows:
				col_name = row.find_all('span')
				col_name = [cell.text.strip() for cell in col_name]
				col_val = row.find_all('td')
				col_val = [cell.text.strip() for cell in col_val]
				date = col_val[0]
				col_val.pop(0)
				# keys aren't sequential in dict
				five_day_data.append(col_val)
				if (len(five_day_data) == 5):
					break
		return five_day_data
	except Exception as e:
		print('Failed, exception: ', str(e))


points = {
	'open' : 0,
	'high' : 1,
	'low' : 2,
	'close' : 3,
	'adj_close' : 4,
	'volume' : 5
}
days = {
	'mon' : 4,
	'friday' : 0
}
def scrape(stock_list):
	data = {}
	for each_stock in stock_list:
		stock_points = scrape_yahoo(each_stock)
		# week open > week close
		if stock_points[4][0] > stock_points[0][3]:
			data[each_stock] = stock_points
			print(each_stock)
			print("------")
		time.sleep(1)													# Use delay to avoid getting flagged as bot
	return data

	


def pairs_trading_algo():

	#Specify paper trading environment
	os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
	#Insert API Credentials
	api = tradeapi.REST('PKAIFPLIOKD855N1EAQN', 'odUHy5tE7qzTfCgXToKmD7wKR7RQ3THPRRLkEahw', api_version='v2') # or use ENV Vars shown below
	account = api.get_account()


	# TODO: get all stocks from nasdaq
	stock_list = []
	url = ('https://finance.yahoo.com/screener/unsaved/a5a8fe09-189d-4314-8ff7-93ebed97d9f8?offset=0&count=100')
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	div = soup.find('div', class_='Ovx(a) Ovx(h)--print Ovy(h) W(100%)')
	table = div.find('table')
	body = table.find('tbody')
	rows = body.find_all('tr')
	for row in rows:
		symbol = row.find('a')
		symbol = symbol.text.strip()
		stock_list.append(symbol)
	stock_data = scrape(stock_list)
	pprint.pprint(stock_data)


	#Trading_algo
	portfolio = api.list_positions()
	# example position
	# {
	#     "asset_id": "904837e3-3b76-47ec-b432-046db621571b",
	#     "symbol": "AAPL",
	#     "exchange": "NASDAQ",
	#     "asset_class": "us_equity",
	#     "avg_entry_price": "100.0",
	#     "qty": "5",
	#     "side": "long",
	#     "market_value": "600.0",
	#     "cost_basis": "500.0",
	#     "unrealized_pl": "100.0",
	#     "unrealized_plpc": "0.20",
	#     "unrealized_intraday_pl": "10.0",
	#     "unrealized_intraday_plpc": "0.0084",
	#     "current_price": "120.0",
	#     "lastday_price": "119.0",
	#     "change_today": "0.0084"
	# }
	clock = api.get_clock()
	# api.submit_order(symbol = 'AAPL',qty = 10,side = 'buy',type = 'market',time_in_force ='gtc',
	#   order_class="bracket",take_profit={"limit_price" : 130},stop_loss={"stop_price": 114})



if __name__ == '__main__':
	pairs_trading_algo()
