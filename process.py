import datetime
import csv
from urllib.request import urlopen
from urllib.parse import quote_plus

def day_down(close):
    day = 0
    prev_close = None
    day_down = []
    for close_price in close:
        if prev_close != None: 
            if close_price < prev_close:
                day += 1
                prev_close = close_price
            else:
                if day > 0:
                    day_down.append(day)
                    day = 0
                prev_close = close_price
        else:
            prev_close = close_price
    return max(day_down)
    
def print_file(file_out, rezult):
    if file_out:
        with open(file_out, 'w') as f_out:
            f_out.write(str(rezult))
    print(rezult)

def process_network(symbol, year, file_out, file_log, level_log):
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    url = "http://www.google.com/finance/historical?q={0}&startdate={1}&enddate={2}&output=csv"
    url = url.format(symbol.upper(), quote_plus(start.strftime('%b %d, %Y')), quote_plus(end.strftime('%b %d, %Y')))
    data = urlopen(url).readlines()
    close_prices = []
    for row in data[1:]:
        x=float(row.decode().strip().split(',')[4])
        close_prices.append(x)
    day = day_down(close_prices)
    print_file(file_out, day)
    
def process_file(file, file_out, file_log, level_log):
    with open(file) as f:
        f.readline()
        csv_file = csv.reader(f, delimiter=',')
        close_prices = []
        for row in csv_file:
            x=float(row[4])
            close_prices.append(x)
    day = day_down(close_prices) 
    print_file(file_out, day)