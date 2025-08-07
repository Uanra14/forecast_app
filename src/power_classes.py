"""
This module implements classes that represent power objects that can be traded or aggregated.
"""
from operator import attrgetter
import json

with open('../data/clean/power_tech_parameters.json', 'r') as f:
    tech_params = json.load(f)

class PowerTech:
    def __init__(self, fuel_cost, co2_intensity, eff_high, eff_low,
                other_costs, carbon_cost):
        self.fuel_cost = float(fuel_cost)
        self.co2_intensity = float(co2_intensity)
        self.eff_high = float(eff_high)
        self.eff_low = float(eff_low)
        self.other_costs = float(other_costs)
        self.carbon_cost = float(carbon_cost)

class PowerDemand:
    def __init__(self, demand, time):
        self.demand = demand
        self.time = time
    
class PowerStack:
    def __init__(self, ordered_tech_blocks, demand):
        self.power_stack = ordered_tech_blocks[:demand]
        self.price = self.power_stack[-1].cost if self.power_stack else 0

class PowerPlant:
    """
    Represents an available power plant in the Netherlands at a specific ISP.
    """
    def __init__(self, idx, isp, name, tech, capacity):
        self.idx = idx
        self.name = name
        self.capacity = int(capacity)
        # TODO: Implement a way to record the previous state of the plant (amount of power generated)
        self.isp = isp
        self.tech = PowerTech(**tech_params[tech])

        self.marginal_cost_curve = self.create_marginal_cost_curve()
        
    def create_marginal_cost_curve(self):
        fuel_cost = self.tech.fuel_cost
        co2_intensity = self.tech.co2_intensity
        eff_high = self.tech.eff_high
        eff_low = self.tech.eff_low
        other_costs = self.tech.other_costs
        carbon_cost = self.tech.carbon_cost

        curve = []

        lb = (fuel_cost + co2_intensity * carbon_cost) / eff_high + other_costs
        ub = (fuel_cost + co2_intensity * carbon_cost) / eff_low + other_costs
        
        for i in range(self.capacity):
            curve.append(
                lb + (ub - lb) * i / (self.capacity - 1)
            )
        return curve

class PowerBlock:
    def __init__(self, idx, source: PowerPlant):
        self.idx = idx
        self.tech = source.tech
        self.cost = source.marginal_cost_curve[idx]
        self.source = source

    def sort(tech_blocks):
        return sorted(tech_blocks, key=attrgetter('cost'))