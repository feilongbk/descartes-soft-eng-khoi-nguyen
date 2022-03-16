import pandas
from datetime import date,datetime,time,timedelta
from core.financial_modelling.scenario  import base_scenario
from core.financial_modelling.scenario_generator  import base_scenario_generator
from core.financial_modelling.constants.earthquake_constants import EARTH_RADIUS, DataConstantString,PolicyConstantString
from core.financial_modelling.constants import event_type

from math_utils import haversine_distance
class USGSEarthQuakeScenarioGenerator(base_scenario_generator.BaseScenarioGenerator):
    def __init__(self,parameters,earthquake_dataframe:pandas.DataFrame,earth_radius = EARTH_RADIUS):
        self.parameters = parameters
        self.earthquake_dataframe = earthquake_dataframe
        self.relevant_earthquake_dataframe = None
        self.scenario_data = None
        self.earth_radius = earth_radius
        self.asset_locations = self.parameters[PolicyConstantString.asset_locations] ## iter of tuple: latitude, longitude
        self.max_radius_tolerance_ratio = 1.01
        layer_max_radius_list = [protection_layer[PolicyConstantString.max_radius] for protection_layer in self.parameters[PolicyConstantString.protection_layers]]
        self.max_radius = max(layer_max_radius_list)
        layer_min_magnitude_list = [protection_layer[PolicyConstantString.min_magnitude] for protection_layer in self.parameters[PolicyConstantString.protection_layers]]
        self.max_radius = max(layer_max_radius_list)
        self.min_magnitude = min(layer_min_magnitude_list)

    def compute_min_distance_to_asset_locations(self,latitude,longitude):
        distance_to_all_locations = [haversine_distance.compute(latitude,longitude,asset_location[DataConstantString.latitude],asset_location[DataConstantString.longitude],self.earth_radius) for asset_location in self.asset_locations]
        return min(distance_to_all_locations)
    def generate_data(self):
        ### RETAIN ONLY RELEVANT DATA TO OPTIMIZE PERFORMANCE
        ## Magnitude
        earthquake_dataframe = self.earthquake_dataframe[self.earthquake_dataframe[DataConstantString.mag]>=self.min_magnitude]
        ## DISTANCE
        earthquake_dataframe[DataConstantString.min_distance] = [self.compute_min_distance_to_asset_locations(earthquake_dataframe[DataConstantString.latitude][index_],earthquake_dataframe[DataConstantString.longitude][index_]) for index_ in earthquake_dataframe.index]
        earthquake_dataframe = earthquake_dataframe[earthquake_dataframe[DataConstantString.min_distance]<=self.max_radius*self.max_radius_tolerance_ratio]
        earthquake_dataframe.index = earthquake_dataframe[DataConstantString.id]
        earthquake_dataframe[DataConstantString.datetime] = pandas.to_datetime(earthquake_dataframe[DataConstantString.time]).dt.tz_convert(tz = "UTC").dt.tz_localize(None)
        earthquake_dataframe[DataConstantString.year] = earthquake_dataframe[DataConstantString.datetime].apply(lambda  x:x.year)
        earthquake_dataframe.sort_values(by =[DataConstantString.datetime],inplace = True)

        self.relevant_earthquake_dataframe = earthquake_dataframe

        event_split_by_years = {x:y for x, y in earthquake_dataframe.groupby (DataConstantString.year, as_index = False)}
        self.scenario_data = list()
        for year in event_split_by_years:
            self.scenario_data.append(base_scenario.BaseScenario(scenario_id=year, event_data={event_type.EventType.EARTHQUAKE: event_split_by_years[year]}))


if __name__ == "__main__":
    from data_collecting.usgs import usgs_helper
    earthquake_data = usgs_helper.get_earthquake_data_within_circle(latitude=35.025, longitude=25.763, radius=200, minimum_magnitude=4.5,
                                 end_date=datetime(year=2000, month=10, day=12),start_date = datetime(year = 1990,month = 12,day = 10))
    print(earthquake_data)
    parameters = dict()
    parameters["asset_locations"] = [{DataConstantString.latitude: 35.025,DataConstantString.longitude: 25.763 }]
    parameters["protection_layers"] = [{"max_radius":75,"min_magnitude":5.0},{"max_radius":200,"min_magnitude":6.0}]
    scenario_generator = USGSEarthQuakeScenarioGenerator(parameters,earthquake_dataframe = earthquake_data)
    scenario_generator.generate_data()
    print(scenario_generator.relevant_earthquake_dataframe)
    print(scenario_generator.scenario_data)
    for scenario in scenario_generator.get_data():
        print(scenario.__dict__)



