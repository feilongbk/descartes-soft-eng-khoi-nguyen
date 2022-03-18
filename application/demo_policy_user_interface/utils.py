from datetime import datetime

from src.earthquakes import tools
from src.earthquakes import usgs_api




def simulate_earthquake(policy_parameters: dict, layers: list, locations: list):
    protection_layers = []
    for index_, layer in enumerate(layers):
        protection_layers.append(
            tools.earthquake_policy_module.EarthquakeProtectionLayer(layer_id=index_, max_radius=layer["max_radius"],
                                                                     min_magnitude=layer["min_magnitude"],
                                                                     payout_ratio=layer["payout_ratio"] / 100.0))

    asset_locations = list()
    for index_, location in enumerate(locations):
        asset_locations.append({
            tools.earthquake_policy_module.DataConstantString.latitude: location["latitude"],
            tools.earthquake_policy_module.DataConstantString.longitude: location["longitude"]
        })

    reporting_levels = [tools.earthquake_policy_module.ReportingLevel.EVENT,
                        tools.earthquake_policy_module.ReportingLevel.EVENT_LAYER]
    policy = tools.earthquake_policy_module.MultiAssetEarthquakePolicy(policy_id=policy_parameters["policy_id"],
                                                                       policy_name=policy_parameters["name"],
                                                                       asset_locations=asset_locations,
                                                                       protection_layers=protection_layers,
                                                                       limit=policy_parameters["limit"],
                                                                       reporting_levels=reporting_levels)

    earthquake_data = usgs_api.get_earthquake_data_for_multiple_locations(asset_locations,
                                                                          1.01 * max([x["max_radius"] for x in layers]),
                                                                          0.99 * min(
                                                                              [x["min_magnitude"] for x in layers]),
                                                                          end_date=datetime.utcnow())
    print(len(earthquake_data))
    payouts = tools.compute_payouts(earthquake_data, policy)
    return payouts
