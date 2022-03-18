import os
import joblib
DIR_PATH = os.path.dirname (os.path.realpath (__file__)).replace ("\\", "/")
DATA_ROOT_DIR = DIR_PATH + "/data"
from common_utils.database_utils import sqlite_helper
from common_utils.database_utils import pickledb_helper

DEFAULT_SQLITE_DB_NAME = "DEFAULT_SQLITE.db"
DEFAULT_PICKLE_DB_NAME = "DEFAULT_PICKLE.db"

from sqlalchemy import Table, Column, MetaData
from datetime import datetime, date, timedelta, time
import json
import pandas


class ObjectEncoder (json.JSONEncoder) :

    def default (self, obj) :
        if isinstance (obj, (datetime, date, time)) :
            return obj.isoformat ()
        elif isinstance (obj, timedelta) :
            return (datetime.min + obj).time ().isoformat ()
        elif isinstance (obj, (pandas.DataFrame, pandas.Series)) :
            return obj.to_json ()

        return super (ObjectEncoder, self).default (obj)


ENCODER_LIST = list ()
ENCODER_LIST.append (ObjectEncoder ())


def json_encode (object) :
    result = object
    for encoder in ENCODER_LIST :
        result = encoder.encode (result)
    return result


def get_data_platform_data_dir () :
    try :
        os.makedirs (DATA_ROOT_DIR)
    except :
        pass
    return DATA_ROOT_DIR


def get_data_platform_sqlite_dir () :
    result = get_data_platform_data_dir () + "/sqlite"
    try :
        os.makedirs (result)
    except :
        pass
    return result


def get_data_platform_pickle_db_dir () :
    result = get_data_platform_data_dir () + "/pickle"
    try :
        os.makedirs (result)
    except :
        pass
    return result


def get_data_platform_flat_file_dir () :
    result = get_data_platform_data_dir () + "/flat_file"
    try :
        os.makedirs (result)
    except :
        pass
    return result


def get_data_platform_sqlite_path (db_name = DEFAULT_SQLITE_DB_NAME) :
    result = get_data_platform_sqlite_dir () + "/" + db_name
    return result


def get_data_platform_pickle_path (db_name) :
    result = get_data_platform_pickle_db_dir () + "/" + db_name
    return result

def get_data_platform_flat_file_dir_path(db_name):
    result = get_data_platform_flat_file_dir () + "/" + db_name
    try:
        os.makedirs(result)
    except:
        pass
    return result


def get_data_platform_sqlite_connection (db_name = DEFAULT_SQLITE_DB_NAME) :
    return sqlite_helper.create_connection (get_data_platform_sqlite_dir () + "/" + db_name)


def get_data_platform_pickle_db_connection (db_name = DEFAULT_SQLITE_DB_NAME, auto_dump = False) :
    return pickledb_helper.create_connection (get_data_platform_pickle_db_dir () + "/" + db_name, auto_dump = auto_dump)

def dump_object_to_flat_file(object,key,db_name):
    joblib.dump(object,get_data_platform_flat_file_dir_path(db_name)+f"/{key}.joblib")

def load_object_to_flat_file(key,db_name):
    return joblib.load(get_data_platform_flat_file_dir_path(db_name)+f"/{key}.joblib")

def execute_query_sqlite (query, connection = None) :
    if connection is None :
        with get_data_platform_sqlite_connection () as connection :
            return connection.execute (query)
    return connection.execute (query)


def get_data_frame_from_query_sqlite (query, connection = None) :
    if connection is None :
        with get_data_platform_sqlite_connection () as connection :
            return sqlite_helper.get_dataframe_from_query (query, connection)
    return sqlite_helper.get_dataframe_from_query (query, connection)

def get_table_model(col_data_types, primary_keys):
    col_model_list = []
    for col in col_data_types :
        print (col)
        col_model_list.append (
            Column (col, col_data_types[col], primary_key = col in primary_keys))
    return col_model_list

def get_table_object(table_name,metadata,col_model_list):
    return Table (table_name, metadata, *col_model_list)

def create_sql_table (
        table_name, col_data_types: dict, primary_keys: iter, delete_existing: bool = False,
        db_name: str = DEFAULT_SQLITE_DB_NAME
        ) :
    metadata = MetaData ()
    col_model_list = get_table_model(col_data_types, primary_keys)

    table_object =get_table_object(table_name,metadata,col_model_list)

    if delete_existing :
        delete_query = f"DROP TABLE IF EXISTS {table_name}"
        execute_query_sqlite (delete_query, get_data_platform_sqlite_connection (db_name))
    result = metadata.create_all (sqlite_helper.get_sqlalchemy_engine (get_data_platform_sqlite_path (db_name)))
    print (result)
    return result


def write_key_value (key, value, db_name) :
    conn = get_data_platform_pickle_db_connection (db_name, True)
    conn.set (key, json_encode (value))


def upsert_data_frame_to_db (df: pandas.DataFrame, table, db_name = DEFAULT_SQLITE_DB_NAME) :
    return sqlite_helper.upsert_data_frame_to_db (df, table, None,
                                                  connection = get_data_platform_sqlite_connection (db_name))


def get_value_from_key (key, db_name) :
    conn = get_data_platform_pickle_db_connection (db_name)
    return conn.get (key)


if __name__ == "__main__" :
    # DIRTY UNIT TEST
    print (get_data_platform_data_dir ())
    policy_db_conn = get_data_platform_pickle_db_connection ("POLICY.db", True)
    print (policy_db_conn)
    policy_db_conn.set ("test", { })
    print (policy_db_conn.get ("test"))
    get_data_platform_sqlite_connection ()
    from sqlalchemy import String, Float, Date

    create_sql_table (table_name = "TEMPERATURE_TEST",
                      col_data_types = { "COUNTRY" : String, "DATE" : Date, "HIGH" : Float, "LOW" : Float },
                      primary_keys = ["COUNTRY", "DATE"], delete_existing = True)
