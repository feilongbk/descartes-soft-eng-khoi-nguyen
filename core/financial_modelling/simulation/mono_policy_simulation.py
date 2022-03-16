class MonoPolicySimulator:
    def __init__(self,simulation_id,simulation_name,policy,scenario_generator,statistics_generator):
        self.simulation_id = simulation_id
        self.simulation_name = simulation_name
        self.policy = policy
        self.scenario_generator = scenario_generator
        self.statistics_generator = statistics_generator