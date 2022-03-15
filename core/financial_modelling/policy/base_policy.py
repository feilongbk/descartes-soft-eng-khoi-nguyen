from core.financial_modelling.scenario.base_scenario import BaseScenario,BaseEventSeries
from core.financial_modelling.scenario_payout.base_payout import BaseScenarioPayOut
class BasePolicy():
    def __init__(self):
        pass
    def compute_payout(self,scenario:BaseScenario)->BaseScenarioPayOut:
        return None