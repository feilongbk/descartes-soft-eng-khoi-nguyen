from data_collecting.usgs import usgs_helper
from datetime import date,datetime
import pandas,numpy

#HISTORICAL_MAGNITUDE_INTERVALS = [1.0,1.25,1.5,2.0,3.0,4.0]
HISTORICAL_MAGNITUDE_INTERVALS = [2.0,3.0]

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
    print(min_longitude,max_longitude,usgs_helper.count_data_from_query(query_url))
    return usgs_helper.get_dataframe_from_query(query_url)


def collect_write_full_historical_data(magnitude_scheduler = HISTORICAL_MAGNITUDE_INTERVALS,longitude_step = 0.25):
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
                                                       min (max_longitude + 0.00001, 180), min_magnitude,max_magnitude, start_time,
                                                       end_time)
            all_data.append(df)
            min_longitude += longitude_step
            max_longitude += longitude_step
    all_data = pandas.concat(all_data,axis = 0)
    all_data.drop_duplicates (inplace = True)
    all_data.sort_values(by= "time",key = pandas.to_datetime,inplace = True)
    all_data.reset_index(inplace = True)
    all_data.drop("index",axis = 1,inplace = True)
    return all_data








if __name__ =="__main__":
    collect_write_full_historical_data([4.0,5.0],longitude_step = 1.0)

