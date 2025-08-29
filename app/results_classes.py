import json
import plotly
import plotly.graph_objs as go
import pandas as pd
import streamlit as st


class PowerPlantVisualiser:
    def __init__(self, source_mapping, results, sources_dict):
        self.source_mapping = source_mapping
        self.results = results
        self.sources_dict = sources_dict

    def display_sources(self):
        for source in self.sources_dict.values():
            if source['id'] in self.results:
                st.markdown(f"### {source['emoji']}\n{source['label']}")


class TimeSeriesPlot():
    def __init__(self, timeseries:pd.DataFrame):
        self.timeseries = timeseries
        self.y_label = timeseries.columns[1]
        self.fig = go.Figure(data=[go.Scatter(x=timeseries['time_utc'], y=timeseries[self.y_label])])
        self.figure_json = json.dumps(self.fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == "__main__":
    ts_data = TimeSeriesPlot(pd.read_csv('static/price.csv', parse_dates=True))
    ts_data.fig.show()
