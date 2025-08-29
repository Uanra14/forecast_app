import csv
import json
from market import MarketSimulator
from utils import get_renewables_data

def main():
    with open('../data/clean/timeseries_data_2025.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        timeseries_data = [{
            'time': row['time_utc'], 
            'demand_mw': row['demand_mw'], 
            'solar_production_mw': row['solar_production_mw'],
            'wind_offshore_production_mw': row['wind_offshore_production_mw'],
            'wind_onshore_production_mw': row['wind_onshore_production_mw']
            }
            for row in reader
        ]

    simulator = MarketSimulator(timeseries_data, days=7)
    simulator.run_simulation()

    with open('../outputs/results.json', 'w') as f:
        json.dump(simulator.get_results(), f, indent=4)

if __name__ == "__main__":
    main()