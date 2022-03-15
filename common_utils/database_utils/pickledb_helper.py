import os
import pickledb

DIR_PATH = os.path.dirname (os.path.realpath (__file__)).replace ("\\", "/")
DB_DIR = DIR_PATH + "/data"
DB_PATH = DB_DIR + "/PICKLE_DB.db"
try :
    os.makedirs (DB_DIR)
except :
    pass


def create_connection (db_file = DB_PATH,auto_dump = False) :
    """ create a database connection to a SQLite database """
    conn = pickledb.load(db_file,auto_dump = auto_dump)
    return conn

if __name__ == '__main__':
    ## DIRTY UNIT TEST
    from datetime import datetime
    import pandas
    pickle_db_test = create_connection (auto_dump = True)
    print(pickle_db_test.get("a"))
    pickle_db_test.set ("a",datetime.utcnow().isoformat())
    pickle_db_test.set ("b",100)
    df = pandas.DataFrame()
    df["X"] = [0.1,0.2]
    df["Y"] = [0.3,0.4]
    pickle_db_test.set ("c",df.to_json())
    print(pickle_db_test.get("a"))
    print(pickle_db_test.get("b"))
    df_json = pickle_db_test.get("c")
    df_new = pandas.read_json(df_json)
    print( df)
    print( df_json)
    print( df_new)