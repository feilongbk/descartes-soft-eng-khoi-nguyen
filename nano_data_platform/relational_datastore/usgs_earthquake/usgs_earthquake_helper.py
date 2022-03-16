from sqlalchemy import String, Float, DateTime, Integer

from nano_data_platform import data_platform_helper

TABLE_NAME = "USGS_EARTHQUAKE"

COLUMN_DATA_TYPES = { }
COLUMN_DATA_TYPES["id"] = String
COLUMN_DATA_TYPES["time"] = DateTime
COLUMN_DATA_TYPES["latitude"] = Float
COLUMN_DATA_TYPES["longitude"] = Float
COLUMN_DATA_TYPES["depth"] = Float
COLUMN_DATA_TYPES["mag"] = Float
COLUMN_DATA_TYPES["magType"] = String
COLUMN_DATA_TYPES["magType"] = String
COLUMN_DATA_TYPES["nst"] = Integer
COLUMN_DATA_TYPES["gap"] = Float
COLUMN_DATA_TYPES["dmin"] = Float
COLUMN_DATA_TYPES["rms"] = Float
COLUMN_DATA_TYPES["net"] = String
COLUMN_DATA_TYPES["updated"] = DateTime
COLUMN_DATA_TYPES["place"] = String
COLUMN_DATA_TYPES["type"] = String
COLUMN_DATA_TYPES["horizontalError"] = Float
COLUMN_DATA_TYPES["depthError"] = Float
COLUMN_DATA_TYPES["magError"] = Float
COLUMN_DATA_TYPES["magNst"] = Integer
COLUMN_DATA_TYPES["status"] = String
COLUMN_DATA_TYPES["locationSource"] = String
COLUMN_DATA_TYPES["magSource"] = String

PRIMARY_KEYS = ["id"]


def create_table (delete_if_exists = False) :
    data_platform_helper.create_sql_table (table_name = TABLE_NAME, col_data_types = COLUMN_DATA_TYPES,
                                           primary_keys = PRIMARY_KEYS, delete_existing = delete_if_exists)


if __name__ =="__main__":
    create_table()
