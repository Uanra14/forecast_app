"""
This module implements classes that represent power objects that can be traded or aggregated.
"""
from operator import attrgetter
import json
import matplotlib.pyplot as plt
import numpy as np

with open('../data/clean/power_tech_parameters.json', 'r') as f:
    tech_params = json.load(f)

class PowerDemand:
    def __init__(self, demand, time):
        self.demand = demand
        self.time = time
    
class PowerStack:
    def __init__(self, ordered_tech_blocks, demand):
        self.power_stack = ordered_tech_blocks[:demand]
        self.price = self.power_stack[-1].cost if self.power_stack else 0

    def __len__(self):
        return len(self.power_stack)
    
    def to_string(self):
        return f"PowerStack with {len(self.power_stack)} blocks, price={self.price}"
    
    def to_dict(self):
        unique_sources = {}
        source_counts = {}

        for ordered_block in self.power_stack:
            source = ordered_block.get_source()
            
            # Count occurrences of each source
            if source.idx not in source_counts.keys():
                source_counts[source.idx] = 0
            source_counts[source.idx] += 1
            
            # Store unique source data
            if source.idx not in unique_sources:
                unique_sources[source.idx] = {
                    'count': source_counts[source.idx],
                }
            else:
                # Update the count for existing source
                unique_sources[source.idx]['count'] = source_counts[source.idx]

        return {
            'sources': unique_sources
        }
    
    def get_last_block(self):
        return self.power_stack[-1] if self.power_stack else None
    
class PowerPlant():
    """
    Represents an available power plant in the Netherlands at a specific ISP.
    """
    def __init__(self, isp, name, tech_name, capacity, idx):
        self.idx = idx
        self.name = name
        self.capacity = int(capacity)
        # TODO: Implement a way to record the previous state of the plant (amount of power generated)
        self.isp = isp

        self.tech_name = tech_name
        self.fuel_cost = float(tech_params[tech_name]['fuel_cost'])
        self.co2_intensity = float(tech_params[tech_name]['co2_intensity'])
        self.eff_high = float(tech_params[tech_name]['eff_high'])
        self.eff_low = float(tech_params[tech_name]['eff_low'])
        self.other_costs = float(tech_params[tech_name]['other_costs'])
        self.carbon_cost = float(tech_params[tech_name]['carbon_cost'])

        self.marginal_cost_curve = self.create_marginal_cost_curve()

    def to_dict(self):
        return {
            'idx': self.idx,
            'name': self.name,
            'tech_name': self.tech_name,
            'capacity': self.capacity,
            'fuel_cost': self.fuel_cost,
            'co2_intensity': self.co2_intensity,
            'eff_high': self.eff_high,
            'eff_low': self.eff_low,
            'other_costs': self.other_costs,
            'carbon_cost': self.carbon_cost
        }
        
    def create_marginal_cost_curve(self):
        curve = []

        lb = (self.fuel_cost + self.co2_intensity * self.carbon_cost) / self.eff_high + self.other_costs
        ub = (self.fuel_cost + self.co2_intensity * self.carbon_cost) / self.eff_low + self.other_costs

        for i in range(self.capacity):
            curve.append(
                lb + (ub - lb) * i / (self.capacity - 1)
            )
        return curve
    
    def plot_marginal_cost_curve(self):
        x = np.arange(self.capacity)
        y = self.marginal_cost_curve

        plt.plot(x, y, label=self.name)
        plt.xlabel('Power Block Index')
        plt.ylabel('Marginal Cost')
        plt.title('Marginal Cost Curve')
        plt.legend()
        plt.grid()
        plt.show()
    
class PowerBlock:
    def __init__(self, idx, source: PowerPlant):
        self.idx = idx
        self.cost = source.marginal_cost_curve[idx]
        self.source = source

    def sort(tech_blocks):
        return sorted(tech_blocks, key=attrgetter('cost'))
    
    def to_string(self):
        return f"This power block is from {self.source.name} with cost {self.cost}"
    
    def to_dict(self):
        return {
            'idx': self.idx,
            'cost': self.cost,
            'source': self.source.to_dict()
        }
    
    def get_source(self):
        return self.source