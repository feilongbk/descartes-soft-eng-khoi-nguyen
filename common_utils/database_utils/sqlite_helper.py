import os
import sqlite3

import pandas
from sqlalchemy import create_engine

DIR_PATH = os.path.dirname (os.path.realpath (__file__)).replace ("\\", "/")
DB_DIR = DIR_PATH + "/data"
DB_PATH = DB_DIR + "/DEFAULT_DB.db"
try :
    os.makedirs (DB_DIR)
except :
    pass


def create_connection (db_file = DB_PATH) :
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect (db_file)
    return conn


def get_sqlalchemy_connection (db_file = DB_PATH) :
    return create_connection (db_file)


def get_sqlalchemy_engine (db_file = DB_PATH) :
    return create_engine (f'''sqlite:///{db_file}''')


def get_dataframe_from_query (query: str, connection = None) -> pandas.DataFrame :
    if connection is None :
        with get_sqlalchemy_connection () as connection :
            return pandas.read_sql (sql = query, con = connection)
    return pandas.read_sql (sql = query, con = connection)


def execute_query (query: str, connection = None) -> pandas.DataFrame :
    if connection is None :
        with get_sqlalchemy_connection () as connection :
            return connection.execute (query)
    return connection.execute (query)


def write_data_frame_to_db (df: pandas.DataFrame, table, schema, connection = None, if_exists = "append") :
    if connection is None :
        with get_sqlalchemy_connection () as connection :
            return df.to_sql (name = table, con = connection, if_exists = if_exists)
    return df.to_sql (name = table, schema = schema, con = connection, if_exists = if_exists, index = False)


if __name__ == '__main__' :
    create_connection ()
