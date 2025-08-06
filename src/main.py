import json
from market import PriceForecaster

def main():
    with open('../data/clean/demand.json', mode='r', encoding='utf-8') as f:
        demand_data = json.load(f)

    forecaster = PriceForecaster(demand_data)
    forecaster.generate_forecast()

    for forecast in forecaster.forecasts:
        print(f"ISP Demand: {forecast['demand']}, Time: {forecast['time']}, Price: {forecast['price']}")

if __name__ == "__main__":
    main()