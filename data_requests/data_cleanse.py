import pandas as pd

"""
Function to clean data for templated csv file manipulation
"""


def default_data():
    my_list = []

    for chunk in pd.read_csv('../data/AllShipments.csv', error_bad_lines=False, chunksize=20000, low_memory=False):
        my_list.append(chunk)

    df = pd.concat(my_list, axis=0)
    cleaned_data_file = df[[
        'FILE NO', 'DIVISION', 'METHOD OF TRANSPORT',
        'BUSINESS LINE', 'SALESMAN NAME', 'REPORT DATE',
        'CUSTOMER NAME', 'PORT OF LOAD NAME', 'PORT OF DCHG NAME',
        'REVENUE', 'EXPENSE', 'PROFIT', 'TOTAL REVENUE LESS DUTIES',
        'TOTAL BILLED TO ACCOUNT', 'TOTAL DUTY BILLED', 'GROSS WEIGHT',
        'TOT CBM', 'CONTAINER COUNT', 'CONTAINER TYPE', 'TOT KGS'
    ]]

    del my_list

    cleaned_data_file.to_csv('../data/AllShipments_cleaned.csv')

    return cleaned_data_file
