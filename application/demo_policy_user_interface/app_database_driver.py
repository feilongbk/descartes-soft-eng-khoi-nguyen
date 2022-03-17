
from sqlalchemy import create_engine
from sqlalchemy import Table
from flask_sqlalchemy import SQLAlchemy
from nano_data_platform import data_platform_helper

def get_db_url():
    return 'sqlite:///' + data_platform_helper.get_data_platform_sqlite_path()
def get_engine():
    return create_engine(get_db_url())

DB_ENGINE = get_engine()
APP_NAME = "DEMO_APP"
USER_TABLE_NAME = f"DEMO_APP_USER"

DB = SQLAlchemy()


class DEMO_APP_USER(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(15), unique=True)
    email = DB.Column(DB.String(50), unique=True)
    password = DB.Column(DB.String(80))

USER_TABLE_OBJECT = Table(USER_TABLE_NAME, DEMO_APP_USER.metadata)

def create_user_table():
    DEMO_APP_USER.metadata.create_all(DB_ENGINE)

def init_database():
    create_user_table()


if __name__ =="__main__":
    pass