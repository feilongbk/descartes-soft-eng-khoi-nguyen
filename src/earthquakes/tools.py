import math

import pandas

from core.financial_modelling.policy.earthquake import multi_asset_earthquake_policy as earthquake_policy

EARTH_RADIUS = 6378

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"


# POINT TO POINT
def compute_haversine(latitude_1, longitude_1, latitude_2, longitude_2, radius):
    phi_1 = math.radians(latitude_1)
    phi_2 = math.radians(latitude_2)
    lambda_1 = math.radians(longitude_1)
    lambda_2 = math.radians(longitude_2)
    sin_half_delta_phi = math.sin((phi_2 - phi_1) * 0.5)
    sin_half_delta_lambda = math.sin((lambda_2 - lambda_1) * 0.5)
    cos_latitude_1 = math.cos(phi_1)
    cos_latitude_2 = math.cos(phi_2)
    h = sin_half_delta_phi ** 2 + cos_latitude_1 * cos_latitude_2 * (sin_half_delta_lambda ** 2)
    return 2 * radius * math.asin(math.sqrt(h))


def get_haversine_distance(latitude_list, longitude_list, center_latitude, center_longitude):
    if not len(latitude_list) == len(longitude_list):
        raise Exception(
            f"Latitude and Longitude must have the same size: {len(latitude_list)} vs {len(longitude_list)} ")
    result = list()
    for lat, long in zip(latitude_list, longitude_list):
        print(lat, long)
        result.append(compute_haversine(lat, long, center_latitude, center_longitude, EARTH_RADIUS))
    return result



def compute_payouts(earthquake_data: pandas.DataFrame, payout_structure:earthquake_policy.MultiAssetEarthquakePolicy) -> pandas.DataFrame:

    pass


def compute_burning_cost():
    pass


if __name__ == "__main__":
    print(get_haversine_distance([1, 3], [2, 5], 3, 4))

    payout_structure_df = pandas.DataFrame([{"Radius":100},])
