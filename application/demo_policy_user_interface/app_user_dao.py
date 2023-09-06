import add_to_path
from sqlalchemy.sql import select

from werkzeug.security import generate_password_hash
from application.demo_policy_user_interface.app_database_driver import *


def insert_user(username, password, email):
    hashed_password = generate_password_hash(password, method='sha256')
    ins = USER_TABLE_OBJECT.insert().values(
        username=username, email=email, password=hashed_password)
    conn = DB_ENGINE.connect()
    conn.execute(ins)
    conn.close()

def update_user(username, password, email):
    hashed_password = generate_password_hash(password, method='sha256')
    ins = USER_TABLE_OBJECT.update().where(USER_TABLE_OBJECT.c.username==username).values(
         email=email, password=hashed_password)
    conn = DB_ENGINE.connect()
    conn.execute(ins)
    conn.close()

def upsert_user(username, password, email):
    try:
        insert_user (username, password, email)
    except Exception as e:
        print(e)
        update_user (username, password, email)




def del_user(username):
    delete = USER_TABLE_OBJECT.delete().where(USER_TABLE_OBJECT.c.username == username)
    conn = DB_ENGINE.connect()
    conn.execute(delete)
    conn.close()


def show_users():
    select_st = select([USER_TABLE_OBJECT.c.username, USER_TABLE_OBJECT.c.email])
    conn = DB_ENGINE.connect()
    rs = conn.execute(select_st)
    for row in rs:
        print(row)
    conn.close()

if __name__ =="__main__":
    show_users()
    upsert_user("user_001","password_001","email_001@abcxyz.com")
    upsert_user("user_002","password_002","email_002@abcxyz.com")
    upsert_user("user_003","password_003","email_003@abcxyz.com")
    show_users()
