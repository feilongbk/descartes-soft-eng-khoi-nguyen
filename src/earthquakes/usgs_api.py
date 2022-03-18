from datetime import datetime, date, time
from io import BytesIO
from urllib.request import Request as URLLIBRequest
from urllib.request import  urlopen
import aiohttp
import asyncio
import pandas

USGS_DATETIME_FORMAT = "%Y-%m-%d"

class USGSQuery:
    # Time

    updatedafter = "updatedafter"
    endtime = "endtime"
    starttime = "starttime"

    # Location
    minlatitude = "minlatitude"
    minlongitude = "minlongitude"
    minlongitude = "minlongitude"
    maxlatitude = "maxlatitude"
    maxlongitude = "maxlongitude"

    # Circle
    latitude = "latitude"
    longitude = "longitude"
    maxradius = "maxradius"
    maxradiuskm = "maxradiuskm"
    # Other
    minmagnitude = "minmagnitude"
    maxmagnitude = "maxmagnitude"


def build_usgs_api_query_url(query_elements: dict, format: str = "csv"):
    result = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
    result = f"{result}format={format}"
    for key in query_elements:
        value = query_elements[key]
        if isinstance(value, date) or isinstance(value, datetime) or isinstance(value, time):
            #value = value.strftime(USGS_DATETIME_FORMAT)
            value = value.isoformat()
        result = f"{result}&{key}={value}"
    return result




def format_output(df):
    df.drop_duplicates (inplace = True)

    df.sort_values (by = "time", inplace = True, key = pandas.to_datetime)
    df.reset_index (inplace = True)
    df.drop ("index", axis = 1, inplace = True)
    return df
def get_dataframe_from_query(query_url):

        url_request = URLLIBRequest (query_url)
        byte_stream = urlopen (url_request).read ()
        df = pandas.read_csv (BytesIO (byte_stream))
        format_output(df)

        return df


def get_query_url_for_circle_search(    latitude: float,
        longitude: float,
        radius: float,
        minimum_magnitude: float,
        end_date,start_date=datetime(1900,1,1)):
    query_elements = dict()
    query_elements[USGSQuery.minmagnitude] = minimum_magnitude
    query_elements[USGSQuery.latitude] = latitude
    query_elements[USGSQuery.longitude] = longitude
    query_elements[USGSQuery.starttime] = start_date ### NEED IT
    query_elements[USGSQuery.endtime] = end_date
    query_elements[USGSQuery.maxradiuskm] = radius
    query_url = build_usgs_api_query_url(query_elements, format="csv")
    return query_url

def get_earthquake_data(
        latitude: float,
        longitude: float,
        radius: float,
        minimum_magnitude: float,
        end_date,start_date=datetime(1900,1,1)) -> pandas.DataFrame:
    query_url = get_query_url_for_circle_search(        latitude=latitude,
        longitude=longitude,
        radius=radius,
        minimum_magnitude=minimum_magnitude,
        end_date=end_date,start_date=start_date)
    return get_dataframe_from_query(query_url)

import asyncio

async def get_earthquake_data_async_multi_location(asset_locations, radius,minimum_magnitude,end_date,start_date = datetime(1900,1,1)):
        result = list ()
        async with aiohttp.ClientSession () as session :
            for asset_location in asset_locations :
                query_url = get_query_url_for_circle_search (latitude = asset_location[USGSQuery.latitude], longitude = asset_location[USGSQuery.longitude],
                                                             radius = radius, minimum_magnitude = minimum_magnitude,
                                                             end_date = end_date, start_date = start_date)

                async with session.get (query_url) as response :
                        byte_stream = await response.read ()
                        df = pandas.read_csv (BytesIO (byte_stream))
                        result.append(df)
        result = pandas.concat(result,axis = 0,ignore_index = True)
        format_output(result)
        loop = asyncio.new_event_loop()
        return result

def get_earthquake_data_for_multiple_locations(asset_locations, radius,minimum_magnitude,end_date,start_date = datetime(1900,1,1)):
    return asyncio.run (get_earthquake_data_async_multi_location (asset_locations, radius,minimum_magnitude,end_date,start_date))


if __name__ == "__main__":
    print("step 1")
    result = get_earthquake_data(latitude=35.025, longitude=25.763, radius=200, minimum_magnitude=4.5,
                                 end_date=datetime(year=2021, month=10, day=21))
    print(result)
    asset_locations = [{"latitude":35.025,"longitude":25.763},{"latitude":35.0,"longitude":25.0}]
    multi_result = asyncio.run(get_earthquake_data_async_multi_location(asset_locations, 200,4.5,end_date=datetime(year=2021, month=10, day=21) ))
    multi_result_1 = get_earthquake_data_for_multiple_locations(asset_locations, 200,4.5,end_date=datetime(year=2021, month=10, day=21) )
    print("multi",multi_result)
    print("multi",multi_result_1)