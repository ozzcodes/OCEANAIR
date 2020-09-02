import pyodbc
import pandas as pd


def data_query():
    # Connect to the NGDashboard database in IES Drive
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\Access\NGDashboard.accdb;')

    cur = conn.cursor()
    # query = cursor.execute('select * from AllShipments')
    query = 'select * from AllShipments'

    df = pd.read_sql(query, conn)
    print(df.head())

    '''For printing out the results to the terminal'''
    # for row in cursor.fetchall():
    #     print(row)

    excel_file = df.to_csv("AllShipments.csv", index=False, index_label='FILE NO')

    return excel_file
