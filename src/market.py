"""
This module simulates the market and generates prices.
"""
from power_classes import PowerBlock, PowerStack, PowerPlant
from utils import ProgressBar
import json

# Load sources from a JSON file
with open('../data/clean/sources.json', 'r') as f:
    sources = json.load(f)


class ISP:
    def __init__(self, demand, solar_production, wind_offshore_production,
                 wind_onshore_production, time, prev_isp=None):
        
        self.demand = int(float(demand))
        self.solar_production = int(float(solar_production))
        self.wind_offshore_production = int(float(wind_offshore_production))
        self.wind_onshore_production = int(float(wind_onshore_production))

        self.time = time
        self.power_blocks = []
        self.prev_isp = prev_isp

        self.sources = [
            PowerPlant(self, **{k: v for k, v in source.items() if k != "emoji"})
            for source in sources
        ]

        for source in self.sources:
            for i in range(source.capacity):
                self.power_blocks.append(PowerBlock(i, source))

        self.power_blocks = PowerBlock.sort(self.power_blocks)
        # Current quantification of solar production, it just subtracts from demand (assumes 0 cost of solar and no curtailment)
        self.power_stack = PowerStack(self.power_blocks, self.demand - self.solar_production - 
                                      self.wind_offshore_production - self.wind_onshore_production)

        self.price = self.power_stack.price
        self.price_setter = self.power_stack.get_last_block().get_source()


    def to_string(self):
        return f"demand = {self.demand}, time = {self.time}, price = {self.price}, sources = {len(self.sources)}, power_stack = {self.power_stack.to_string()} \n" \
               f"The last block in the stack: {self.power_stack.get_last_block().to_string()}"
    

    def to_dict(self):
        return {
            'demand': self.demand,
            'solar_production': self.solar_production,
            'wind_offshore_production': self.wind_offshore_production,
            'wind_onshore_production': self.wind_onshore_production,
            'time': self.time,
            'price': self.price,
            'price_setter': self.price_setter.idx,
            'power_stack': self.power_stack.to_dict()
        }


class MarketSimulator:
    def __init__(self, timeseries_data, days=7):
        self.results = []
        self.periods = days * 24 * 4

        self.timeseries = [data['time'] for data in timeseries_data]
        self.demand = [data['demand_mw'] for data in timeseries_data]
        self.solar_production = [data['solar_production_mw'] for data in timeseries_data]
        self.wind_offshore_production = [data['wind_offshore_production_mw'] for data in timeseries_data]
        self.wind_onshore_production = [data['wind_onshore_production_mw'] for data in timeseries_data]


    def simulate_ISP(self, demand, solar_production, wind_offshore_production, 
                     wind_onshore_production, time, prev_isp=None):
        
        isp = ISP(prev_isp=prev_isp, demand=demand, solar_production=solar_production, wind_offshore_production=wind_offshore_production, wind_onshore_production=wind_onshore_production, time=time)
        self.results.append(isp.to_dict())


    def run_simulation(self):
        progress_bar = ProgressBar(total=self.periods, desc="Simulating ISPs")

        for i in range(self.periods):
            self.simulate_ISP(self.demand[i], self.solar_production[i],
                             self.wind_offshore_production[i], self.wind_onshore_production[i], 
                             self.timeseries[i])
            
            progress_bar.update()
        progress_bar.close()


    def get_results(self):
        return self.results