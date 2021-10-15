import os
import csv

def clean():
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
		csv_file.close()
	skip = True
	for stock in stock_symbols:
		if stock == 'VOSO':
			skip = False
		if skip:
			continue
		else:
			with open('Historic_Data/' + stock + '.csv') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				line_count = 0

				for row in csv_reader:
					if line_count == 0:
						if row[0] != 'Date':
							os.remove('Historic_Data/' + stock + '.csv')
						line_count += 1
			csv_file.close()




if __name__ == '__main__':
	clean()