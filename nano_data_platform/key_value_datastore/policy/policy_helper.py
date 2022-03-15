import pandas

DB_NAME ="POLICY.db"
from datetime import  datetime,date
import copy
from nano_data_platform import data_platform_helper
from json import JSONEncoder
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H%M%S"

def format_policy_data(policy_data:dict):
    formatted_data = copy.deepcopy(policy_data)
    for key in formatted_data:
        if isinstance(formatted_data[key],datetime):
            formatted_data[key] = formatted_data[key].strftime (DATETIME_FORMAT)
        if isinstance(formatted_data[key],date):
            formatted_data[key] = formatted_data[key].strftime (DATE_FORMAT)
    return formatted_data
def write_data(policy_id,policy_data:dict):
    return data_platform_helper.write_key_value(policy_id,policy_data,DB_NAME)

def get_policy_data(policy_id):
    return data_platform_helper.get_value_from_key(policy_id,DB_NAME)

if __name__ =="__main__":
    test_policy = {}
    test_policy["id"] ="test_policy"
    test_policy["policy_name"] ="test_policy"
    test_policy["inception_date"] = datetime(year = 2020,month = 1,day = 1).date()
    test_policy["expiry_date"] = datetime(year = 2020,month = 12,day = 31)
    test_policy["contract_type"] = "EARTH_QUAKE"
    test_policy["asset_locations"] = [(50.0,60.0),(40.0,10.0)]
    test_policy["limit"] = 100
    test_policy["data_frame"] = pandas.DataFrame()
    test_policy["data_frame"]["A"] = [0.1,1.0]
    test_policy["data_frame"]["B"] = [0.1,1.5]
    test_policy["protection_layers"] = [{"max_radius":50.0,"min_magnitude":4.5,"payout":1.0},{"max_radius":100.0,"min_magnitude":6.0,"payout":0.75},{"max_radius":200,"min_magnitude":7.0,"payout":0.5}]
    write_data("test_policy",test_policy)
    print(get_policy_data("test_policy"))

