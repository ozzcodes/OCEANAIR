import pandas as pd

data_file = '../data/Unbilled_cleaned.csv'


def query_unbilled():
    df = pd.read_csv(data_file, low_memory=False).reset_index(
        drop=True).drop(columns='Unnamed: 0')

    format_dict = {
        col_name: '{:,.2f}' for col_name in df.select_dtypes(float).columns
    }

    format_dict['DIVISION'] = int
    format_dict['GROSS WEIGHT'] = int
    format_dict['SALESMAN CODE'] = int
    format_dict['BUSINESS LINE'] = int

    df['REPORT DATE'] = pd.to_datetime(df['REPORT DATE'])

    """
    Obtain the date timeframes of arrival and invoice to make checks
    to see if the delivered shipment file has been billed or not
    """

