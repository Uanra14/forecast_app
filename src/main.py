import csv
from market import MarketSimulator

def main():
    with open('../data/clean/demand.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        demand_data = [row for row in reader]

    simulator = MarketSimulator(demand_data)
    simulator.generate_price_forecast()

    for forecast in simulator.forecasts[:20]:
        print(f"ISP Demand: {forecast['demand']}, Time: {forecast['time']}, Price: {forecast['price']}")

if __name__ == "__main__":
    main()
    