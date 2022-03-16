import math

import pandas

from core.financial_modelling.constants.earthquake_constants import EARTH_RADIUS, PolicyConstantString
from core.financial_modelling.policy.earthquake import multi_asset_earthquake_policy as earthquake_policy_module
from core.financial_modelling.scenario_generator.earthquake import usgs_earthquake_scenario_generator

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"


# POINT TO POINT
def compute_haversine (latitude_1, longitude_1, latitude_2, longitude_2, radius) ->float:
    phi_1 = math.radians (latitude_1)
    phi_2 = math.radians (latitude_2)
    lambda_1 = math.radians (longitude_1)
    lambda_2 = math.radians (longitude_2)
    sin_half_delta_phi = math.sin ((phi_2 - phi_1) * 0.5)
    sin_half_delta_lambda = math.sin ((lambda_2 - lambda_1) * 0.5)
    cos_latitude_1 = math.cos (phi_1)
    cos_latitude_2 = math.cos (phi_2)
    h = sin_half_delta_phi ** 2 + cos_latitude_1 * cos_latitude_2 * (sin_half_delta_lambda ** 2)
    return 2 * radius * math.asin (math.sqrt (h))

def get_haversine_distance (latitude_list, longitude_list, center_latitude, center_longitude) ->list:
    if not len (latitude_list) == len (longitude_list) :
        raise Exception (
            f"Latitude and Longitude must have the same size: {len (latitude_list)} vs {len (longitude_list)} ")
    result = list ()
    for lat, long in zip (latitude_list, longitude_list) :
        result.append (compute_haversine (lat, long, center_latitude, center_longitude, EARTH_RADIUS))
    return result

def compute_payouts (
        earthquake_data: pandas.DataFrame, policy: earthquake_policy_module.MultiAssetEarthquakePolicy
) -> pandas.Series :
    scenario_parameters = dict ()
    scenario_parameters[PolicyConstantString.asset_locations] = policy.asset_locations
    scenario_parameters[PolicyConstantString.protection_layers] = [
        { PolicyConstantString.max_radius : layer.max_radius, PolicyConstantString.min_magnitude : layer.min_magnitude }
        for layer in policy.protection_layers]
    scenario_generator = usgs_earthquake_scenario_generator.USGSEarthQuakeScenarioGenerator (
        parameters = scenario_parameters, earthquake_dataframe = earthquake_data)
    result = policy.compute_payout_multi_scenario (scenario_generator.get_data ())
    return result.apply (lambda x : x.scenario_payout)

def compute_burning_cost (payouts: (dict, pandas.Series), start_year, end_year) ->float:
    if len(payouts) == 0:
        return 0.0
    if isinstance (payouts, dict) :
        payouts = pandas.Series (payouts)
    return ((payouts.index >= start_year) * (payouts.index <= end_year) * payouts).sum () / (end_year - start_year + 1)


if __name__ == "__main__" :
    print (get_haversine_distance ([1, 3], [2, 5], 3, 4))

    layer_1 = earthquake_policy_module.EarthquakeProtectionLayer (layer_id = 1, max_radius = 10.0, min_magnitude = 4.5,
                                                                  payout_ratio = 1.0)
    layer_2 = earthquake_policy_module.EarthquakeProtectionLayer (layer_id = 2, max_radius = 50.0, min_magnitude = 5.5,
                                                                  payout_ratio = 0.75)
    layer_3 = earthquake_policy_module.EarthquakeProtectionLayer (layer_id = 3, max_radius = 200.0, min_magnitude = 6.5,
                                                                  payout_ratio = 0.5)
    protection_layers = [layer_1, layer_2, layer_3]
    asset_locations = list ()
    asset_locations.append ({
        earthquake_policy_module.DataConstantString.latitude : 35.025,
        earthquake_policy_module.DataConstantString.longitude : 25.763
    })
    asset_locations.append ({
        earthquake_policy_module.DataConstantString.latitude : 36,
        earthquake_policy_module.DataConstantString.longitude : 25.7
    })
    asset_locations.append ({
        earthquake_policy_module.DataConstantString.latitude : 35.3,
        earthquake_policy_module.DataConstantString.longitude : 25.76
    })
    asset_locations = pandas.DataFrame (asset_locations)
    print (asset_locations)
    print (layer_1.__dict__)
    print (layer_2.__dict__)
    print (layer_3.__dict__)
    reporting_levels = [earthquake_policy_module.ReportingLevel.EVENT,
                        earthquake_policy_module.ReportingLevel.EVENT_LAYER]
    policy_1 = earthquake_policy_module.MultiAssetEarthquakePolicy (policy_id = 1, policy_name = "policy 1",
                                                                    asset_locations = asset_locations,
                                                                    protection_layers = protection_layers, limit = 100,
                                                                    reporting_levels = reporting_levels)
    print (policy_1.__dict__)

    from data_collecting.usgs import usgs_helper
    from datetime import datetime

    earthquake_data = usgs_helper.get_earthquake_data_within_circle (latitude = 35.025, longitude = 25.763,
                                                                     radius = 200, minimum_magnitude = 4.5,
                                                                     end_date = datetime (year = 2021, month = 12,
                                                                                          day = 31),
                                                                     start_date = datetime (year = 1911, month = 1,
                                                                                            day = 1))
    payouts = compute_payouts (earthquake_data, policy_1)
    print (payouts)
    print (compute_burning_cost (payouts, 1950, 2021))
    print (compute_burning_cost (payouts, 1990, 2021))
