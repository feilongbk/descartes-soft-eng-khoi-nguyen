from data_collecting.usgs import usgs_helper
from datetime import date,datetime
import pandas,numpy
from common_utils.database_utils import sqlite_helper
from nano_data_platform.relational_datastore.usgs_earthquake import usgs_earthquake_helper
from nano_data_platform import data_platform_helper

#HISTORICAL_MAGNITUDE_INTERVALS = [1.0,1.25,1.5,2.0,3.0,4.0]
HISTORICAL_MAGNITUDE_INTERVALS = [2.0,2.5,4.0, 1000.0]
API_LIMIT = 20000

def format_collected_data(df):
    df.drop_duplicates (inplace = True)
    df.sort_values(by= "time",key = pandas.to_datetime,inplace = True)
    df.reset_index(inplace = True)
    df.drop("index",axis = 1,inplace = True)

def collect_historical_data_under_constraints(min_longitude, max_longitude,min_magnitude,max_magnitude,start_time,end_time):
    query_elements = dict()
    if min_magnitude is not None:
        query_elements[usgs_helper.USGSQuery.minmagnitude] = min_magnitude
    if max_magnitude is not None:
        query_elements[usgs_helper.USGSQuery.maxmagnitude] = max_magnitude
    query_elements[usgs_helper.USGSQuery.minlongitude] = min_longitude
    query_elements[usgs_helper.USGSQuery.maxlongitude] = max_longitude
    query_elements[usgs_helper.USGSQuery.starttime] = start_time
    query_elements[usgs_helper.USGSQuery.endtime] = end_time
    query_url = usgs_helper.build_usgs_api_query_url(query_elements)
    nb_of_rows = usgs_helper.count_data_from_query(query_url)
    if nb_of_rows>= API_LIMIT:
        print("From",min_longitude,"To",max_longitude,":",nb_of_rows,f"rows of magnitude in {min_magnitude,max_magnitude}. Data exceeds API limit, splitting query into 2 subqueries by longitude")
        a =  collect_historical_data_under_constraints(min_longitude, 0.5*(min_longitude+max_longitude), min_magnitude,max_magnitude,start_time,end_time)
        b = collect_historical_data_under_constraints(0.5*(min_longitude+max_longitude),max_longitude, min_magnitude,max_magnitude,start_time,end_time)
        result = pandas.concat([a,b],axis=0,ignore_index=True)
        format_collected_data(result)
        return result
    print("From",min_longitude,"To",max_longitude,":",nb_of_rows,f"row(s) of magnitude in {min_magnitude,max_magnitude}")
    return usgs_helper.get_dataframe_from_query(query_url)


def collect_full_historical_data(magnitude_scheduler = HISTORICAL_MAGNITUDE_INTERVALS, longitude_step = 30.0):
    start_time = date(year = 1900,month = 1,day = 1)
    end_time = datetime.utcnow()

    for i in range(len(magnitude_scheduler)-1):
        all_data = list ()
        min_magnitude = magnitude_scheduler[i]
        max_magnitude = magnitude_scheduler[i + 1]
        min_longitude = -180
        max_longitude = min_longitude + longitude_step
        while max_longitude <= 180 :
            df = collect_historical_data_under_constraints (max (min_longitude - 0.00001, -180),
                                                       min (max_longitude + 0.00001, 180), min_magnitude-0.0001,max_magnitude+0.0001, start_time,
                                                       end_time)
            all_data.append(df)
            min_longitude += longitude_step
            max_longitude += longitude_step
    all_data = pandas.concat(all_data,axis = 0)
    format_collected_data(all_data)
    return all_data





if __name__ =="__main__":
    #collect_full_historical_data([4.0, 1000.0], longitude_step = 30.0)
    #data_df = collect_full_historical_data(HISTORICAL_MAGNITUDE_INTERVALS, longitude_step = 30.0)
    data_df = collect_full_historical_data([4.0, 1000.0], longitude_step = 30.0)
    #data_df = collect_full_historical_data([4.0,4.01], longitude_step = 180.0)
    result = data_platform_helper.upsert_data_frame_to_db(data_df, usgs_earthquake_helper.TABLE_NAME)
    print(result)
    #data_platform_helper.sqlite_helper.write_data_frame_to_db(data_df,usgs_earthquake_helper.TABLE_NAME,None,connection=data_platform_helper.get_data_platform_sqlite_connection())
