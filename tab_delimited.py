import csv

with open('tab_delimited_file.txt', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        date = row[0]
        symbol = row[1]
        closing_price = float(row[2])

#For files with a header in the file
with open('colon_delimited_file.txt', 'rb') as f:
    reader = csv.DictReader(f, delimiter=':')
    for row in reader:
        date = row[0]
        symbol = row[1]
        closing_price = row[2]


today_prices = {'AAPL' : 90.91, 'MSFT' : 41.68, 'FB' : 64.5 }

with open('comma_delimted_file.txt', 'wb') as f:
    writer = csv.writer(f, delimiter=',')
