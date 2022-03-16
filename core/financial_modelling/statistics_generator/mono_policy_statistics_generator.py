class MonoPolicyStatisticsGenerator :
    def __init__ (self, simulation_data) :
        self.simulation_data = simulation_data
        self.statistics_data = None

    def generate_data (self) :
        pass

    def get_data (self, recompute = False) :
        if self.statistics_data is None or recompute :
            self.generate_data ()
        return self.statistics_data
