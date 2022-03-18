from datetime import date, datetime
import add_to_path
import numpy
import pandas

from math_utils import haversine_distance
from src.earthquakes import usgs_api


def test_query_url_builder():
    target_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2021-01-01"
    query_elements = dict()
    query_elements[usgs_api.USGSQuery.starttime] = date(year=2021, month=1, day=1)
    assert usgs_api.build_usgs_api_query_url(query_elements) == target_url


def test_get_earthquake_data():
    EARTH_RADIUS = 6378
    start_date = datetime(year=1950, month=1, day=1)
    end_date = datetime(year=2000, month=1, day=1)
    latitude = 35.025
    longitude = 25.763
    radius = 200
    minimum_magnitude = 4.5

    result = usgs_api.get_earthquake_data(latitude=latitude, longitude=longitude, radius=radius,
                                          minimum_magnitude=minimum_magnitude,
                                          end_date=end_date, start_date=start_date)

    result["datetime"] = pandas.to_datetime(result["time"]).dt.tz_localize(None)
    result["distance"] = [haversine_distance.compute(result["latitude"][index_],
                                                     result["longitude"][index_], latitude,
                                                     longitude, EARTH_RADIUS) for index_ in result.index]

    assert len(result) > 0
    assert result["distance"].min() <= radius * 1.01  ## TOLERANCE FOR AVERAGE EARTH RADIUS ERROR
    assert result["datetime"].min() >= start_date
    assert result["datetime"].max() <= end_date
    assert result["mag"].min() >= minimum_magnitude
    print(result.columns)

def test_get_earthquake_data_multi():
    EARTH_RADIUS = 6378
    start_date = datetime(year=1950, month=1, day=1)
    end_date = datetime(year=2000, month=1, day=1)
    latitude = 35.025
    longitude = 25.763
    radius = 200
    minimum_magnitude = 4.5

    mono_asset_location_result = usgs_api.get_earthquake_data(latitude=latitude, longitude=longitude, radius=radius,
                                          minimum_magnitude=minimum_magnitude,
                                          end_date=end_date, start_date=start_date)

    asset_location_list_1 = [{"latitude":latitude,"longitude":longitude},{"latitude":latitude,"longitude":longitude}]
    multi_asset_location_result_1= usgs_api.get_earthquake_data_for_multiple_locations(asset_location_list_1,radius=radius,
                                          minimum_magnitude=minimum_magnitude,
                                          end_date=end_date, start_date=start_date)

    ## Same location = no difference
    assert len(mono_asset_location_result) == len(multi_asset_location_result_1)
    assert numpy.square(mono_asset_location_result["mag"] - multi_asset_location_result_1["mag"]).sum() == 0.0
    asset_location_list_2 = [{"latitude":latitude,"longitude":longitude},{"latitude":latitude+1.0,"longitude":longitude+1.0}]
    multi_asset_location_result_2= usgs_api.get_earthquake_data_for_multiple_locations(asset_location_list_2,radius=radius,
                                          minimum_magnitude=minimum_magnitude,
                                          end_date=end_date, start_date=start_date)
    ## 2 locations >= 1 location
    assert len(mono_asset_location_result) <= len(multi_asset_location_result_2)
    assert mono_asset_location_result["mag"].sum() <= multi_asset_location_result_2["mag"].sum()
