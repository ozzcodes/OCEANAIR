from time import sleep
from configparser import ConfigParser
from data_requests.data_import import data_query
import pandas as pd
from sqlalchemy import create_engine


# #### Not necessary for this data upload #### #
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def pg_load_table():
    # Create sqlalchemy engine connection to postgres
    engine = create_engine('postgresql+psycopg2://postgres:0212181@localhost:5432/postgres')

    csv_file = '../data/AllShipments.csv'

    df = pd.read_csv(csv_file, index_col="FILE NO", error_bad_lines=False, dtype='unicode')
    load_data = df.to_sql('ytd_data', con=engine, if_exists='replace', index=True, index_label='FILE NO')
    df.drop_duplicates(load_data)

    print(df.index)


# Run the main function to import the newly generated CSV file into the SQL Database
if __name__ == '__main__':
    data_query()
    sleep(10)
    pg_load_table()
