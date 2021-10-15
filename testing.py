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
    # data = [ {01-01-2000: [open, high, low, close, adj_close, vol], ...}, ...]
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
    return x[3]


def test():
    data = organize_data()
    weeks = get_weeks()
    counter = 0
    success = 0
    crash = 0
    up = 0

    for week in weeks:

        # finding potentials for next week
        for stock in data:
            if week in stock:
                stock_week = stock[week]
                open = float(stock_week[0])
                high = float(stock_week[1])
                low = float(stock_week[2])
                close = float(stock_week[3])
                if low <= open * 0.9:
                    crash += 1
                elif high >= open * 1.02:
                    success += 1
                elif close > open:
                    up += 1

                counter += 1
    print('total count: ' + str(counter))
    print('success ratio: ' + str(float(success) / counter))
    print('up ratio: ' + str(float(up) / counter))
    print('crash ratio: ' + str(float(crash) / counter))


if __name__ == '__main__':
    test()
