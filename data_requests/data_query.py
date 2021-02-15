import pandas as pd
from datetime import datetime, date

"""
Create a function to query specific data
"""


def query_division(div):
    df = pd.read_csv('../data/AllShipments_cleaned.csv', low_memory=False)
    format_dict = {
        col_name: '{:,.2f}' for col_name in df.select_dtypes(float).columns
    }
    format_dict['DIVISION'] = int
    format_dict['GROSS_WEIGHT'] = int

    df['REPORT DATE'] = pd.to_datetime(df['REPORT DATE'])
    df = df.query(f"DIVISION == {div}").reset_index(drop=True).drop(columns='Unnamed: 0')

    return df


def query_sales(sales_group):
    return sales_group


if __name__ == '__main__':
    print(query_division(10))
