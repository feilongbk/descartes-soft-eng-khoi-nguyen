import pandas


class BaseEventSeries(pandas.DataFrame):
    def get_event_type(self):
        return self.event_type
    pass

class BaseScenario:
    def __init__(self,scenario_id,event_data:dict):
        self.scenario_id = scenario_id
        self.event_data = event_data ## DICTIONARY OF EVENT SERIES BY EVENT CODE

if __name__ =="__main__":

    pass
