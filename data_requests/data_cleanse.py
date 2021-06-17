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
        'BUSINESS LINE', 'SALESMAN CODE', 'SALESMAN NAME', 'REPORT DATE',
        'CUSTOMER CODE', 'CUSTOMER NAME', 'PORT OF LOAD NAME', 'PORT OF DCHG NAME',
        'REVENUE', 'EXPENSE', 'PROFIT', 'TOTAL REVENUE LESS DUTIES',
        'TOTAL BILLED TO ACCOUNT', 'TOTAL DUTY BILLED', 'GROSS WEIGHT',
        'TOT CBM', 'CONTAINER COUNT', 'CONTAINER TYPE', 'TOT KGS'
    ]]

    del my_list

    cleaned_data_file.to_csv('../data/AllShipments_cleaned.csv')

    return cleaned_data_file


def unbilled_data():
    my_list = []

    for chunk in pd.read_csv(r'R:\Austin_CustomReports\Unbilled_Data\UnbilledDailyData.csv',
                             error_bad_lines=False, chunksize=20000, low_memory=False):
        my_list.append(chunk)

    df = pd.concat(my_list, axis=0)

    unbilled_file_headers = df[[
        'FILE NO', 'DIVISION', 'MODE OF TRANSPORTATION',
        'BUSINESS LINE', 'SALESMAN CODE', 'SALESMAN NAME', 'REPORT DATE',
        'CUSTOMER CODE', 'CUSTOMER NAME', 'PORT OF LOAD NAME', 'PORT OF LOAD COUNTRY',
        'PORT OF DCHG NAME', 'PORT OF DCHG COUNTRY', 'GROSS WEIGHT', 'REVENUE',
        'PROFIT', 'TOTAL BILLED TO ACCOUNT', 'STATUS', 'CONTROLLER',
        'INV DATE', 'DATE INVOICED', 'LAST EVENT NAME'
    ]]

    del my_list

    unbilled_file_headers.to_csv('../data/Unbilled_cleaned.csv')

    return unbilled_file_headers
