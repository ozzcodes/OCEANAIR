import pandas as pd
from datetime import datetime, date

"""
Create a function to query specific data
"""


def query_division(div):
    """
    :rtype: division to be filtered
    """
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


def query_customer(customer_name: list):
    """
    :param customer_name: a list of customer codes to query customer data
    """
    df_customer = pd.read_csv('../data/AllShipments_cleaned.csv',
                              low_memory=False).reset_index(
        drop=True).drop(columns='Unnamed: 0').dropna(subset=['CUSTOMER CODE'])

    df_customer = df_customer[df_customer['CUSTOMER CODE'].str.contains('|'.join(customer_name))]

    start_date = "2020-06-01"
    end_date = "2021-05-31"
    df = df_customer[(df_customer['REPORT DATE'] > start_date) &
                     (df_customer['REPORT DATE'] <= end_date)].reset_index(drop=True)

    df.to_csv(f"../data/customer_data_queries/{customer_name}.csv", index='FILE NO')


# Customer codes to search for
customer_codes = ['AKOBIO02', 'AKOBIO01', 'AKOBIO03', 'AKOYA02']

if __name__ == '__main__':
    print(query_division(10))
    print(query_customer(customer_name=customer_codes))
