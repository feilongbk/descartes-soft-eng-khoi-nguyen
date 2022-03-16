import pandas

from core.financial_modelling.scenario.base_scenario import BaseScenario,BaseEventSeries
from core.financial_modelling.scenario_simulation.base_scenario_simulation import BaseScenarioPayOut
class BasePolicy():
    def __init__(self):
        pass
    def compute_payout(self,scenario:BaseScenario)->BaseScenarioPayOut:
        return None

    '''/** Return scenario payout with scenario ID 
    scenarios: list, iter, dict, series of BaseScenario
    '''
    def compute_payout_multi_scenario(self,scenarios:(list,iter,dict,pandas.Series))->pandas.Series:
        scenario_list = scenarios
        if isinstance(scenario_list,dict):
            scenario_list = list(scenario_list.values())
        if isinstance(scenario_list,pandas.Series):
            scenario_list = list(scenario_list.values)

        result = {scenario.scenario_id:self.compute_payout(scenario) for scenario in scenario_list}
        return pandas.Series(result)
