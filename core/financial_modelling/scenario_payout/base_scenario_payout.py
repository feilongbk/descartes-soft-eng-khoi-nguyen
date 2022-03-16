import pandas
class PayOutData(pandas.DataFrame):
    pass
class BaseScenarioPayOut:
    def __init__(self,scenario_id,scenario_payout:float,payout_data:dict):
        self.scenario_id = scenario_id
        self.payout_data = payout_data
        self.scenario_payout = scenario_payout