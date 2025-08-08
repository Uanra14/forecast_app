import csv
import json
from market import MarketSimulator

def main():
    with open('../data/clean/demand.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        demand_data = [row for row in reader]

    simulator = MarketSimulator(demand_data)
    simulator.generate_price_forecast()

    with open('../outputs/results.json', 'w') as f:
        json.dump(simulator.to_dict(), f, indent=4)

if __name__ == "__main__":
    main()
    