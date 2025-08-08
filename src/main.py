import csv
from market import MarketSimulator

def main():
    with open('../data/clean/demand.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        demand_data = [row for row in reader]

    simulator = MarketSimulator(demand_data)
    simulator.generate_price_forecast()

    for isp in simulator.isps:
        print(isp.to_string())

    # Plot the marginal cost curves for the power plant activated in the last ISP
    last_isp = simulator.isps[-1]
    last_isp.power_stack.get_last_block().source.plot_marginal_cost_curve()

if __name__ == "__main__":
    main()
    