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
    format_dict['SALESMAN CODE'] = int

    df['REPORT DATE'] = pd.to_datetime(df['REPORT DATE'])
    df = df.query(f"DIVISION == {div}").reset_index(drop=True).drop(columns='Unnamed: 0')

    return df


def query_sales():
    df_sales = pd.read_csv('../data/AllShipments_cleaned.csv',
                           low_memory=False).reset_index(drop=True).drop(columns='Unnamed: 0')

    format_dict = {
        col_name: '{:,.2f}' for col_name in df_sales.select_dtypes(float).columns
    }

    format_dict['SALESMAN CODE'] = int
    df_sales['REPORT DATE'] = pd.to_datetime(df_sales['REPORT DATE'])

    # df_new = df_sales[[
    #     'SALESMAN NAME', 'REPORT DATE', 'METHOD OF TRANSPORT', 'DIVISION',
    #     'BUSINESS LINE', 'CUSTOMER NAME', 'PORT OF LOAD NAME', 'PORT OF DCHG NAME',
    #     'REVENUE', 'EXPENSE', 'PROFIT', 'TOTAL REVENUE LESS DUTIES',
    #     'TOTAL BILLED TO ACCOUNT', 'TOTAL DUTY BILLED', 'GROSS WEIGHT',
    #
    # ]]

    # column_names = [
    #     'SALESMAN_NAME', 'REPORT_DATE', 'METHOD_OF_TRANSPORT', 'DIVISION',
    #     'CUSTOMER_NAME', 'REVENUE', 'EXPENSE', 'PROFIT'
    # ]

    print(df_sales.index)

    column_names = [
        'SALESMAN_CODE', 'REVENUE', 'EXPENSE', 'PROFIT'
    ]

    sales_data = pd.DataFrame(columns=column_names)

    for data in df_sales:
        salesman = data['SALESMAN CODE']
        # report_date = data['REPORT DATE']['REPORT_DATE']
        # customer = data['CUSTOMER NAME']['CUSTOMER_NAME']
        # method_transport = data['METHOD OF TRANSPORT']['METHOD_OF_TRANSPORT']
        # div = data['DIVISION']['DIVISION']
        rev = data['REVENUE']['REVENUE']
        exp = data['EXPENSE']['EXPENSE']
        profit = data['PROFIT']['PROFIT']

        sales_data = sales_data.append({
            'SALESMAN_CODE': salesman,
            # 'REPORT_DATE': report_date,
            # 'CUSTOMER_NAME': customer,
            # 'METHOD_OF_TRANSPORT': method_transport,
            # 'DIVISION': div,
            'REVENUE': rev,
            'EXPENSE': exp,
            'PROFIT': profit,
        }, ignore_index=True)

    print(sales_data.head(20))


def query_dates():
    df_date = pd.read_csv('../data/AllShipments_cleaned.csv',
                          low_memory=False).reset_index(
        drop=True).drop(columns='Unnamed: 0').dropna(subset=['REPORT DATE'])

    start_date = "1/1/2019"
    end_date = "3/31/2021"

    after_start_date = df_date['REPORT DATE'] >= start_date
    before_end_date = df_date['REPORT DATE'] <= end_date

    timeframe = after_start_date & before_end_date
    df_date = df_date[df_date['REPORT DATE']]

    return df_date


def query_customer(customer_name, timeframe):
    df_customer = pd.read_csv('../data/AllShipments_cleaned.csv',
                              low_memory=False).reset_index(
        drop=True).drop(columns='Unnamed: 0').dropna(subset=['CUSTOMER NAME'])

    df_customer = df_customer[df_customer['CUSTOMER NAME'].str.contains(customer_name)]
    df_customer.to_csv(f"{customer_name}.csv", index='FILE NO')


if __name__ == '__main__':
    print(query_division(10))
    # query_sales()
    print(query_customer('WELLPET LLC', timeframe=query_dates()))

