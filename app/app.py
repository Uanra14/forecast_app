from flask import Flask, render_template, request
from results_classes import TimeSeriesPlot
import pandas as pd

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hist', methods=["GET", "POST"])
def hist():
    day_ahead_prices = pd.read_csv('static/price.csv', parse_dates=True)
    fig = TimeSeriesPlot(day_ahead_prices).fig

    if request.method == "POST":
        start_date = request.form.get('start_date')
        if not start_date:
            start_date = day_ahead_prices['time_utc'].min()
            
        end_date = request.form.get('end_date')
        if not end_date:
            end_date = day_ahead_prices['time_utc'].max()
    else:
        start_date = day_ahead_prices['time_utc'].min()
        end_date = day_ahead_prices['time_utc'].max()

    filtered_data = day_ahead_prices[(day_ahead_prices['time_utc'] >= start_date) & (day_ahead_prices['time_utc'] <= end_date)]
    fig = TimeSeriesPlot(filtered_data).fig

    return render_template('hist.html', fig=fig.to_html(full_html=False),
                            start_date=start_date,
                            end_date=end_date)
