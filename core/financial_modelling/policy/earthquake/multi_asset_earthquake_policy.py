from datetime import date, datetime

import pandas,numpy

from core.financial_modelling.policy.base_policy import BasePolicy, BaseEventSeries, BaseScenario, BaseScenarioPayOut
from math_utils import haversine_distance
from core.financial_modelling.constants import event_type

## CONSTANT STRINGS FOR EarthquakePolicy

EARTH_RADIUS = 6378

class ConstantString :
    time = "time"
    latitude = "latitude"
    longitude = "longitude"
    depth = "depth"
    mag = "mag"
    magType = "magType"
    nst = "nst"
    gap = "gap"
    dmin = "dmin"
    rms = "rms"
    net = "net"
    id = "id"
    updated = "updated"
    place = "place"
    type = "type"
    horizontalError = "horizontalError"
    depthError = "depthError"
    magError = "magError"
    magNst = "magNst"
    status = "status"
    locationSource = "locationSource"
    magSource = "magSource"

class AggregationRule:
    max ="max"
    sum ="sum"
    mean ="mean"

class ReportingLevel:
    EVENT = "EVENT"
    EVENT_LAYER = "EVENT_LAYER"
    EVENT_LAYER_LOCATION = "EVENT_LAYER_LOCATION"


def aggregate(df:pandas.DataFrame, rule):
    agg_dim = len(df.shape)-1
    if rule ==AggregationRule.max:
        return df.max(axis = agg_dim)
    if rule ==AggregationRule.sum:
        return df.sum(axis = agg_dim)
    if rule ==AggregationRule.mean:
        return df.mean(axis = agg_dim)
    return None


class EarthquakeProtectionLayer :
    def __init__ (self, layer_id, max_radius, min_magnitude, payout_ratio) :
        self.layer_id = layer_id
        self.max_radius = max_radius
        self.min_magnitude = min_magnitude
        self.payout_ratio = payout_ratio

    def compute_payout (
            self, event_series: BaseEventSeries, location_latitude, location_longitude
    ) -> pandas.DataFrame :
        distances = [haversine_distance.compute (event_series[ConstantString.latitude][index_],
                                                 event_series[ConstantString.longitude][index_], location_latitude,
                                                 location_longitude, EARTH_RADIUS) for index_ in event_series.index]
        distances = pandas.Series (index = event_series.index, data = distances)

        payout_ratio_series = self.payout_ratio * (distances <= self.max_radius) * (
                    event_series[ConstantString.mag] >= self.min_magnitude)
        payout_ratio_series.name = f'LAYER_{self.layer_id}'
        return payout_ratio_series


class MultiAssetEarthquakePolicy (BasePolicy) :
    def __init__ (
            self, policy_id, policy_name, asset_locations:pandas.DataFrame, limit: float, protection_layers: iter,
            inception_date: date = None, expiry_date: date = None, currency = "USD", ignore_date = True,
            location_aggregation_rule = "max",  layer_aggregation_rule = "max", event_aggregation_rule = "max",reporting_levels:list = None
    ) :
        self.policy_id = policy_id
        self.policy_name = policy_name
        if isinstance(asset_locations,pandas.DataFrame):
            self.asset_locations = asset_locations.to_dict(orient ="records")
        elif isinstance(asset_locations,list):
            self.asset_locations = list(asset_locations)
        self.inception_date = inception_date
        self.expiry_date = expiry_date
        self.limit = limit
        self.protection_layers = protection_layers
        self.currency = currency
        self.ignore_date = ignore_date
        self.location_aggregation_rule = location_aggregation_rule
        self.layer_aggregation_rule = layer_aggregation_rule
        self.event_aggregation_rule = event_aggregation_rule
        self.reporting_levels = reporting_levels
    EVENT_TYPE = event_type.EventType.EARTHQUAKE

    def compute_payout (self, scenario: BaseScenario) -> BaseScenarioPayOut :
        loss_by_event_layer = dict()
        loss_by_event_layer_location = dict()
        event_series = scenario.event_data[self.EVENT_TYPE]
        event_series = event_series.drop_duplicates()
        event_series.index  = event_series[ConstantString.id]
        for layer in self.protection_layers:
            loss_by_event_layer_location[layer.layer_id] = dict()
            for location_index,location in enumerate(self.asset_locations):
                elem_payout = self.limit*layer.compute_payout (event_series, location[ConstantString.latitude],location[ConstantString.longitude])
                elem_payout.name = f"{elem_payout.name}_LOCATION_{location_index}"
                loss_by_event_layer_location[layer.layer_id][location_index] =elem_payout
            tmp_df = pandas.concat(loss_by_event_layer_location[layer.layer_id].values(),axis = 1)
            loss_by_event_layer_location[layer.layer_id] = tmp_df
            ### Aggregate over asset locations
            loss_by_event_layer[layer.layer_id] = aggregate(tmp_df,self.location_aggregation_rule)
                
            loss_by_event_layer[layer.layer_id] = numpy.minimum(loss_by_event_layer[layer.layer_id],self.limit) ## PAYOUT CANNOT EXCESS LIMIT

        print("loss_by_event_layer_location",loss_by_event_layer_location)

        loss_by_event_layer = pandas.DataFrame(loss_by_event_layer)
        print("loss_by_event_layer",loss_by_event_layer)
        ### Aggregate over all layers
        loss_by_event = aggregate(loss_by_event_layer,self.layer_aggregation_rule)
        print (loss_by_event)
        ### Aggregate over all events
        loss = aggregate(loss_by_event,self.event_aggregation_rule)
        print (loss)

        detailed_analysis  = dict()
        detailed_analysis[ReportingLevel.EVENT] = loss_by_event
        detailed_analysis[ReportingLevel.EVENT_LAYER] = loss_by_event_layer
        detailed_analysis[ReportingLevel.EVENT_LAYER_LOCATION] = loss_by_event_layer_location
        if self.reporting_levels is None or len(self.reporting_levels)==0:
            payout_data = None
        else:
            payout_data = dict()
            for reporting_level in self.reporting_levels:
                payout_data[reporting_level] = detailed_analysis[reporting_level]


        result = BaseScenarioPayOut(scenario_id = scenario.scenario_id,scenario_payout = loss,payout_data = payout_data)
        return result


if __name__ == "__main__" :
    layer_1 = EarthquakeProtectionLayer (layer_id = 1, max_radius = 10.0, min_magnitude = 4.5, payout_ratio = 1.0)
    layer_2 = EarthquakeProtectionLayer (layer_id = 2, max_radius = 50.0, min_magnitude = 5.5, payout_ratio = 0.75)
    layer_3 = EarthquakeProtectionLayer (layer_id = 3, max_radius = 200.0, min_magnitude = 6.5, payout_ratio = 0.5)
    protection_layers = [layer_1, layer_2, layer_3]
    asset_locations = list()
    asset_locations.append({ConstantString.latitude:35.025, ConstantString.longitude:25.763})
    asset_locations.append({ConstantString.latitude:36, ConstantString.longitude:25.7})
    asset_locations.append({ConstantString.latitude:35.3, ConstantString.longitude:25.76})
    asset_locations  = pandas.DataFrame(asset_locations)
    print(asset_locations)
    print (layer_1.__dict__)
    print (layer_2.__dict__)
    print (layer_3.__dict__)
    reporting_levels = [ReportingLevel.EVENT,ReportingLevel.EVENT_LAYER,ReportingLevel.EVENT_LAYER_LOCATION]
    reporting_levels = [ReportingLevel.EVENT,ReportingLevel.EVENT_LAYER]
    policy_1 = MultiAssetEarthquakePolicy (policy_id = 1, policy_name = "policy 1", asset_locations = asset_locations,
                                           protection_layers = protection_layers, limit = 100,reporting_levels = reporting_levels)

    print (policy_1.__dict__)

    # Event Series
    event_series = pandas.DataFrame ()
    event_series[ConstantString.time] = [datetime (year = 2022, month = 2, day = 2),
                                         datetime (year = 2022, month = 5, day = 10)]
    event_series[ConstantString.latitude] = [35., 35.0]
    event_series[ConstantString.longitude] = [25., 25.9]
    event_series[ConstantString.mag] = [5.0, 6.5]
    event_series[ConstantString.id] = ["event_1", "event_2"]

    print (layer_1.compute_payout (event_series, *asset_locations.values[0]))
    print (layer_2.compute_payout (event_series, *asset_locations.values[0]))
    print (layer_3.compute_payout (event_series, *asset_locations.values[0]))

    scenario = BaseScenario(scenario_id = 1, event_data = { event_type.EventType.EARTHQUAKE:event_series})

    print (policy_1.compute_payout (scenario).__dict__)
