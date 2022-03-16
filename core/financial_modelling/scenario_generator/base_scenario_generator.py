import pandas
class BaseScenarioGenerator:
    def __init__(self,parameters:dict,scenario_data:(pandas.Series,dict)=None):
        self.parameters = parameters
        self.scenario_data = scenario_data

    def generate_data(self):
        pass
    def get_data(self,recompute = False):
        if self.scenario_data is None or recompute:
            self.generate_data()
        return self.scenario_data

