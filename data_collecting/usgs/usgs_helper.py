from datetime import datetime, date, time
from io import BytesIO
from urllib.request import Request, urlopen

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


def get_dataframe_from_query(query_url):
    url_request = Request(query_url)
    bytes = urlopen(url_request).read()
    df = pandas.read_csv(BytesIO(bytes))
    return df

def count_data_from_query(query_url):
    count_url = query_url.replace("query?","count?")
    url_request = Request (count_url)
    bytes = urlopen (url_request).read ()
    #print(count_url)
    return int(bytes)

def get_earthquake_data_within_circle(
        latitude: float,
        longitude: float,
        radius: float,
        minimum_magnitude: float,
        end_date,start_date=datetime(1900,1,1) ) -> pandas.DataFrame:
    query_elements = dict()
    query_elements[USGSQuery.minmagnitude] = minimum_magnitude
    query_elements[USGSQuery.latitude] = latitude
    query_elements[USGSQuery.longitude] = longitude
    query_elements[USGSQuery.starttime] = start_date ### NEED IT
    query_elements[USGSQuery.endtime] = end_date
    query_elements[USGSQuery.maxradiuskm] = radius

    query_url = build_usgs_api_query_url(query_elements, format="csv")
    return get_dataframe_from_query(query_url)



if __name__ == "__main__":
    # DIRTY BEHAVIOUR TEST
    query_elements = dict()
    query_elements[USGSQuery.minlatitude] = -90
    query_elements[USGSQuery.starttime] = date(year=2020, month=1, day=1)
    query_elements[USGSQuery.minmagnitude] = 6.0
    print(build_usgs_api_query_url(query_elements))
    query_url = build_usgs_api_query_url(query_elements)
    df = get_dataframe_from_query(query_url)
    print(df)
    print(count_data_from_query(query_url))
