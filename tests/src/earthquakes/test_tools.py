import pytest
import numpy

from src.earthquakes import tools
import pandas
from data_collecting.usgs import usgs_helper
from datetime import datetime
def test_haversine_distance():
    ## REFERENCE https://www.vcalc.com/wiki/vCalc/Haversine+-+Distance
    target_value = 314.4
    computed_value = tools.compute_haversine(latitude_1=1, longitude_1=2, latitude_2=3, longitude_2=4,
                                                 radius=tools.EARTH_RADIUS)
    print(computed_value,target_value,numpy.sign(computed_value-target_value))
    assert pytest.approx( computed_value- target_value, target_value*0.01) == 0.0


    target_value = 2662.2
    computed_value = tools.compute_haversine(latitude_1=50, longitude_1=60, latitude_2=70, longitude_2=80,
                                                 radius=tools.EARTH_RADIUS)
    print(computed_value,target_value,numpy.sign(computed_value-target_value))
    assert pytest.approx(computed_value - target_value, target_value*0.01) == 0.0

def test_compute_payout():

    layer_1 = tools.earthquake_policy_module.EarthquakeProtectionLayer (layer_id = 1, max_radius = 10.0, min_magnitude = 4.5,
                                                                  payout_ratio = 0.8)
    layer_2 = tools.earthquake_policy_module.EarthquakeProtectionLayer (layer_id = 2, max_radius = 50.0, min_magnitude = 5.5,
                                                                  payout_ratio = 0.75)
    layer_3 = tools.earthquake_policy_module.EarthquakeProtectionLayer (layer_id = 3, max_radius = 200.0, min_magnitude = 6.5,
                                                                  payout_ratio = 0.5)
    protection_layers = [layer_1, layer_2, layer_3]
    asset_locations = list ()
    asset_locations.append ({
        tools.earthquake_policy_module.DataConstantString.latitude : 35.025,
        tools.earthquake_policy_module.DataConstantString.longitude : 25.763
    })
    asset_locations.append ({
        tools.earthquake_policy_module.DataConstantString.latitude : 36,
        tools.earthquake_policy_module.DataConstantString.longitude : 25.7
    })
    asset_locations.append ({
        tools.earthquake_policy_module.DataConstantString.latitude : 35.3,
        tools.earthquake_policy_module.DataConstantString.longitude : 25.76
    })
    asset_locations = pandas.DataFrame (asset_locations)
    print (asset_locations)
    print (layer_1.__dict__)
    print (layer_2.__dict__)
    print (layer_3.__dict__)
    reporting_levels = [tools.earthquake_policy_module.ReportingLevel.EVENT,
                        tools.earthquake_policy_module.ReportingLevel.EVENT_LAYER]
    policy_1 = tools.earthquake_policy_module.MultiAssetEarthquakePolicy (policy_id = 1, policy_name = "policy 1",
                                                                    asset_locations = asset_locations,
                                                                    protection_layers = protection_layers, limit = 100,
                                                                    reporting_levels = reporting_levels)
    print (policy_1.__dict__)

    radius_tolerance_ratio = 1.02
    earthquake_data = usgs_helper.get_earthquake_data_within_circle (latitude = 35.025, longitude = 25.763,
                                                                     radius = radius_tolerance_ratio, minimum_magnitude = 4.5,
                                                                     end_date = datetime (year = 2021, month = 12,
                                                                                          day = 31),
                                                                     start_date = datetime (year = 1921, month = 1,
                                                                                            day = 1))
    payouts = tools.compute_payouts (earthquake_data, policy_1)
    print(payouts)

    max_possible_payout = max([layer.payout_ratio * 100 for layer in protection_layers])
    assert max(payouts) <= max_possible_payout
    assert min(payouts) >= 0.0
    nb_of_scenario = 2021 - 1921 + 1
    assert len(payouts) <= nb_of_scenario
    assert min(payouts.index) >= 1921
    assert max(payouts.index) <= 2021
    ## Empty payout: return 0
    assert tools.compute_burning_cost({},1990,2021) == 0.0
    ## start year > end year return 0
    assert tools.compute_burning_cost(payouts,2000,1990) == 0.0
    ## out of simulation range return 0
    assert tools.compute_burning_cost(payouts,1800,1900) == 0.0
    assert tools.compute_burning_cost(payouts,2100,2200) == 0.0
    ## strictly >0 if
    assert tools.compute_burning_cost ({2010:80.0}, 2000, 2020) > 0.0

    years = range (1921, 2021)

    burning_cost_dict = { start_year:tools.compute_burning_cost (payouts, start_year = start_year, end_year = 2021) for start_year in
                          years }
    assert max (burning_cost_dict.values()) <= max_possible_payout
    assert min (burning_cost_dict.values()) >= 0.0
