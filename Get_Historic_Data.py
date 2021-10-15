import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import time
import datetime
from bs4 import BeautifulSoup
import requests
import csv


def get_data():
    stock_symbols = []
    with open('nasdaq_screener_1622168233474.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                stock_symbols.append(row[0])
                line_count += 1
    counter = 0
    skip = True
    for stock in stock_symbols:
        if (stock == 'CHI'):
            skip = False
        if skip:
            continue
        else:
            url = ('https://query1.finance.yahoo.com/v7/finance/download/' + stock + '?period1=946684800&period2=1609372800&interval=1wk&events=history&includeAdjustedClose=true')
            page = requests.get(url, allow_redirects=True)
            open(stock + '.csv', 'wb').write(page.content)
            os.rename(stock + '.csv', '/Users/benwozniak/PersonalProjects/Investing/Historic_Data/' + stock + '.csv')
            counter += 1
            if counter >= 2:
                counter = 0
                time.sleep(1)

        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # driver = webdriver.Chrome(chrome_options=option)
        # driver.get('https://finance.yahoo.com/quote/' + stock + '/history?period1=946684800&period2=1609372800&interval=1wk&filter=history&frequency=1wk&includeAdjustedClose=true')
        # id_box = driver.find_element_by_id()

if __name__ == '__main__':
	get_data()