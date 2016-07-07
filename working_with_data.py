import math
import random
import csv
import dateutil.parser
import datetime

import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from normal_distribution import inverse_normal_cdf
from linear_algebra import shape, get_column, make_matrix
from statistics import correlation


def bucketsize(point, bucket_size):
    """floor the point to the next lower multiple of bucket size"""
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketsize(point, bucket_size) for point in points)


def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title()
    plt.show()


def plot_uni_nor():
    random.seed(0)

    # U(-100, 100)
    uniform = [200 * random.random() - 100 for _ in range(10000)]

    # N(0, 57)
    normal = [57 * inverse_normal_cdf(random.random()) for _ in range(10000)]

    plot_histogram(uniform, 10, "Uniform Histogram")

    plot_histogram(normal, 10, "Normal Histogram")


def random_normal():
    """returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())

'''
xs = [random_normal() for _ in range(1000)]
ys1 = [x + random_normal() / 2 for x in xs]
ys2 = [-x + random_normal() / 2 for x in xs]

plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
plt.xlabel('xs')
plt.ylabel('ys')
plt.legend(loc=9)
plt.title("Very different joint distribution")
plt.show()

print("correlation of xs and ys1 {} and correlation of xs and ys2 {}".format(correlation(xs, ys1),
                                                                             correlation(xs, ys2)))
'''

def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i,j)th entry
    is the correlation between columns i and j of the data"""

    _, num_columns = shape(data)

    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))

    return make_matrix(num_columns, num_columns, matrix_entry)


def visual_approach():
    num_points = 100

    def random_row():
        row = [None, None, None, None]
        row[0] = random_normal()
        row[1] = -5 * row[0] + random_normal()
        row[2] = row[0] + row[1] + 5 * random_normal()
        row[3] = 6 if row[2] > -2 else 0
        return row

    random.seed(0)
    data = [random_row()
            for _ in range(num_points)]
    _, num_columns = shape(data)
    fig, ax = plt.subplots(num_columns, num_columns)

    for i in range(num_columns):
        for j in range(num_columns):

            # Scatter columm_j on the x-axis vs column_i on the y-axis
            if i != j:
                ax[i][j].scatter(get_column(data, j), get_column(data, i))

            # unlesss i == j, in which case show the series name
            else:
                ax[i][j].annotate("series {}".format(i), (0.5, 0.5),
                                  xycoords='axes fraction',
                                  ha="center", va="center")

            # then hide dxis labels except left and bottom charts
            if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
            if j > 0: ax[i][j].yaxis.set_visible(False)

    # fix the bottom right and top left except left and bottom charts
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[1][1].set_xlim(ax[0][1].get_ylim())

    plt.show()


# visual_approach()

def parse_row(input_row, parsers):
    """given a list of parsers (some of which may be None)
    apply the appropriate one to each element of the input_row"""
    return [try_or_none(parser)(value) if parser is not None else value
            for value, parser in zip(input_row, parsers)]


def parse_rows_with(reader, parsers):
    """wrap a reader to apply the parers to each of its rows"""
    #print(reader)
    for row in reader:
        yield parse_row(row, parsers)


def try_or_none(f):
    """Wrap f to return None if f raises an exception
    assumes f takes only one input"""

    def f_or_none(x):
        try:
            return (x)
        except:
            return None

    return f_or_none


def try_parse_field(field_name, value, parser_dict):
    """try to parse value using the appropriate function from parser_dic"""
    parser = parser_dict.get(field_name)  # None if no such entry
    if parser is not None:
        return try_or_none(parser)(value)
    else:
        return value


def parse_dict(input_dict, parser_dict):
    return {field_name: try_parse_field(field_name, value, parser_dict)
            for field_name, value in input_dict.iteritems()}


def picker(field_name):
    """returns a function that picks a field out of a dict"""
    return lambda row: row[field_name]


def pluck(field_name, rows):
    """turn a list of dicts into the list of field_name values"""
    return map(picker(field_name), rows)


def group_by(grouper, rows, value_transform=None):
    # key is output of grouper, value is list of rows
    grouped = defaultdict(list)
    for row in rows:
        grouped[grouper(row)].append(row)
    if value_transform is None:
        return grouped
    else:
        return {key: value_transform(rows)
                for key, rows in grouped.items()}


if __name__ == "__main__":
    data = []
    with open("stock.txt", "r") as f:
        reader = csv.reader(f, delimiter='\t')
        #print(reader)
        for line in parse_rows_with(reader, [None, dateutil.parser.parse, float]):
            print(line)
            data.append({'symbol': line[0], 'date': line[1], 'closing_price': line[2]})
    """
    for row in data:
        if any(x is None for x in row):
            print(row)"""
    re_data = pluck("symbol", data)
    print(list(re_data))
    #data = [{' closing_price': 102.06, 'date': datetime.datetime(2014, 8, 29, 0, 0), 'symbol': 'AAPL'}]

    max_appl_price = max(row['closing_price']
                         for row in data
                         if row['symbol'] == "AAPL")

    by_symbol = defaultdict(list)
    for row in data:
        by_symbol[row['symbol']].append(row)

    max_price_by_symbol = {symbol : max(row['closing_price'] for row in grouped_rows)
                           for symbol, grouped_rows in by_symbol.items()}
    print(max_price_by_symbol)

    max_price_by_symbol = group_by(picker('symbol'),
                                   data,
                                   lambda rows: max(pluck("closing_price", rows)))

    print(max_price_by_symbol)