from flask import Flask, render_template
from results_classes import TimeSeriesPlot
import pandas as pd

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hist')
def hist():
    day_ahead_prices = pd.read_csv('static/price.csv', parse_dates=True)
    ts_plot = TimeSeriesPlot(day_ahead_prices)

    return render_template('hist.html', figure_json=ts_plot.figure_json)

