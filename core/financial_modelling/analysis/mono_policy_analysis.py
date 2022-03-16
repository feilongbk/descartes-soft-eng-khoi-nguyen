class MonoPolicyAnalyzer:
    def __init__(self,analysis_id,analysis_name,policy,scenario_generator,statistics_generator):
        self.analysis_id = analysis_id
        self.analysis_name = analysis_name
        self.policy = policy
        self.scenario_generator = scenario_generator
        self.statistics_generator = statistics_generator