import csv
from csv import reader

filename = "data/Business_ReviewData_2020v2.csv"

with open(filename, 'r') as data:
    for line in csv.DictReader(data):
        print(line)

data.close()

# with open("data/Business_ReviewData_2020v2.csv") as read_obj:
#     csv_read = reader(read_obj)
#     list_of_rows = list(csv_read)
#     print(list_of_rows)
#
# read_obj.close()
