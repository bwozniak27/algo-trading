import os
import csv
import glob
import math


def get_weeks():
  weeks = []
  with open('Historic_Data/AAME.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0

    for row in csv_reader:
      if line == 0:
        line += 1
      else:
        weeks.append(row[0])
    csv_file.close()

  return weeks

# Assemble all csv's into data list


def organize_data():
  directory = os.fsencode('Historic_Data')
  # data = [ {01-01-2000: [open_price, high, low, close, adj_close, vol], ...}, ...]
  data = []
  files = glob.glob("Historic_Data/*.csv")
  for file in files:
    filename = os.fsdecode(file)
    with open(file) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      stock_data = {}
      for row in csv_reader:
        if line_count == 0:
          line_count += 1
        else:
          week = row
          date = week[0]
          week.pop(0)
          stock_data[date] = week
    csv_file.close()
    data.append(stock_data)
  return data


def sorting_function(x):
  return float(x[3])


def backtrade():
  data = organize_data()
  weeks = get_weeks()
  take = 1.25
  loss = 0.85
  money = 2000
  profit_weeks = 0
  beginning_money = money
  potentials = []
  line = 0
  weekly_returns = []
  yearly_returns = []
  year_start_money = money
  year = weeks[0][0:4]
  f = open('results.txt', 'w')

  # loop thru all weeks
  for x in range(len(weeks) - 1):
    # new year
    if weeks[x][0:4] != year:
      yearly_returns.append(float(money) / year_start_money)
      year = weeks[x][0:4]
      year_start_money = money

    # choosing 10 stocks from potentials and calculating week
    if line < 2:
      line += 1
    else:
      starting_money = money

      # $10 - $50
      potentials.sort(key=sorting_function)
      # weekly cash, continue buying until no cash left
      week_cash = starting_money

      # more than 10 potential stocks
      if len(potentials) >= 10:
        
        shares = []
        for i in range(10):
          shares.append(0)
          
        for i in range(-10, -1):
          per_stock = week_cash / abs(i)
          
          num_shares = math.floor(per_stock / float(potentials[i][0]))
          week_cash -= float(potentials[i][0]) * num_shares
          shares[i] = num_shares

        # 50 and down
        for i in range(-10, -1):
          # stock_week = [open_price, high, low, close, adj_close, vol]

          stock_week = potentials[i]
          f.write(str(stock_week) + '\n')
          open_price = float(stock_week[0])
          high = float(stock_week[1])
          low = float(stock_week[2])
          close = float(stock_week[3])
          money -= open_price * shares[i]
          if low <= open_price * loss:
            money += open_price * loss * shares[i]
          elif high >= open_price * take:
            money += open_price * take * shares[i]
            print('take')
          else:
            money += close * shares[i]
            
      # less than 10 potential stocks
      elif len(potentials) != 0:
        
        shares = []
        for i in range(10):
          shares.append(0)

        for i in range(len(potentials)):
          per_stock = week_cash / abs(len(potentials) - i)

          num_shares = math.floor(per_stock / float(potentials[i][0]))
          week_cash -= float(potentials[i][0]) * num_shares
          shares[i] = num_shares
          
        for stock_week in potentials:
          f.write(str(stock_week) + '\n')
          open_price = float(stock_week[0])
          high = float(stock_week[1])
          low = float(stock_week[2])
          close = float(stock_week[3])
          money -= open_price * shares[i]
          if low <= open_price * loss:
            money += open_price * loss * shares[i]
          elif high >= open_price * take:
            money += open_price * take * shares[i]
            print('take')
          else:
            money += close * shares[i]

      weekly_returns.append(float(money) / starting_money)

    potentials = []
    # finding potentials for next week
    for stock in data:
      if weeks[x] in stock:

        # if negative week and vol > 1,000,000 and 10 < price < 50
        if float(stock[weeks[x]][0]) > float(stock[weeks[x]][3]) and float(stock[weeks[x]][5]) > 500000 and float(stock[weeks[x]][3]) > 10 and float(stock[weeks[x]][3]) < 50:

          # need to add the next week
          potentials.append(stock[weeks[x + 1]])

  # TODO factor in taxes
  f.write('starting money: ' + str(beginning_money) + '\n')
  f.write('final money (pre taxes): ' + str(money) + '\n')
  f.write('yearly returns: ' + str(yearly_returns) + '\n')
  f.write('weekly returns: ' + str(weekly_returns) + '\n')
  f.close()


if __name__ == '__main__':
    backtrade()
