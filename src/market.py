"""
This module simulates the market and generates prices.
"""
from power_classes import PowerBlock, PowerStack, PowerSource
import json

# Load sources from a JSON file
with open('../data/clean/sources.json', 'r') as f:
    sources = json.load(f)

### GLOBAL VARIABLES ###
sources = [PowerSource(i, **source) for i, source in enumerate(sources)]

class ISP:
    def __init__(self, demand, time):
        self.demand = int(demand)
        self.time = time
        self.power_blocks = []

        for source in sources:
            for i in range(source.capacity):
                self.power_blocks.append(PowerBlock(i, source))

        self.power_blocks = PowerBlock.sort(self.power_blocks)
        self.power_stack = PowerStack(self.power_blocks, self.demand)
        self.price = self.power_stack.price

class PriceForecaster:
    def __init__(self, demand):
        self.isps = []
        self.demand = demand
        self.periods = len(demand)
        self.forecasts = []
    
    def simulate_ISP(self, demand):
        isp = ISP(**demand)
        self.isps.append(isp)

    def generate_forecast(self):
        for i in range(self.periods):
            self.simulate_ISP(self.demand[i])
        
        for isp in self.isps:
            self.forecasts.append({
                'demand': isp.demand,
                'time': isp.time,
                'price': isp.price,
            })