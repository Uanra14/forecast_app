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
    def __init__(self, demand, time, prev_isp=None):
        self.demand = int(float(demand))
        self.time = time
        self.power_blocks = []
        self.prev_isp = prev_isp

        self.sources = [PowerPlant(self, **source) for source in sources]

        for source in self.sources:
            for i in range(source.capacity):
                self.power_blocks.append(PowerBlock(i, source))

        self.power_blocks = PowerBlock.sort(self.power_blocks)
        self.power_stack = PowerStack(self.power_blocks, self.demand)
        
        self.price = self.power_stack.price
        self.price_setter = self.power_stack.get_last_block().get_source()

    def to_string(self):
        return f"demand = {self.demand}, time = {self.time}, price = {self.price}, sources = {len(self.sources)}, power_stack = {self.power_stack.to_string()} \n" \
               f"The last block in the stack: {self.power_stack.get_last_block().to_string()}"
    
    def to_dict(self):
        return {
            'demand': self.demand,
            'time': self.time,
            'price': self.price,
            'price_setter': self.price_setter.idx,
            'power_stack': self.power_stack.to_dict()
        }

class MarketSimulator:
    def __init__(self, demand):
        self.isps = []
        self.demand = demand
        self.periods = len(demand)
        self.forecasts = []
    
    def simulate_ISP(self, demand, prev_isp=None):
        isp = ISP(prev_isp=prev_isp, **demand)
        self.isps.append(isp)

    def generate_price_forecast(self):
        progress_bar = ProgressBar(total=self.periods, desc="Simulating ISPs")
        for i in range(self.periods):
            self.simulate_ISP(self.demand[i], self.isps[i-1] if i > 0 else None)
            progress_bar.update()
        progress_bar.close()

    def to_dict(self):
        return {
            'isps': [isp.to_dict() for isp in self.isps],
        }
