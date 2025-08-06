"""
This module implements classes that represent power objects that can be traded or aggregated.
"""
from operator import attrgetter
import numpy as np

class PowerDemand:
    def __init__(self, demand, time):
        self.demand = demand
        self.time = time
    
class PowerStack:
    def __init__(self, ordered_tech_blocks, demand):
        self.power_stack = ordered_tech_blocks[:demand]
        self.price = self.power_stack[-1].cost if self.power_stack else 0
    
class PowerSource:
    def __init__(self, idx, name, tech, capacity):
        self.idx = idx
        self.name = name
        self.tech = tech
        self.capacity = int(capacity)
        self.marginal_cost_curve = self.create_marginal_cost_curve()
        
    def create_marginal_cost_curve(self):
        return np.linspace(0, self.capacity - 1, self.capacity)

class PowerBlock:
    def __init__(self, idx, source: PowerSource):
        self.idx = idx
        self.tech = source.tech
        self.cost = source.marginal_cost_curve[idx]
        self.source = source

    def sort(tech_blocks):
        return sorted(tech_blocks, key=attrgetter('cost'))