import json
import streamlit as st
import plotly.express as px

# Load sources from a JSON file
with open('../data/clean/sources.json', 'r') as f:
    sources = json.load(f)

# Load the results from a JSON file
with open('../outputs/price_forecast.json', 'r') as f:
    results = json.load(f)

### GLOBAL VARIABLES ###
SOURCE_NUM = len(sources)
COLUMN_NUM = 8
ROW_NUM = (SOURCE_NUM + COLUMN_NUM - 1) // COLUMN_NUM

# initialise a streamlit dashboard
st.set_page_config(
    page_title='DA Market Forecast',
    page_icon=':high_voltage:',
)

st.header("NL Energy Market Digital Twin")
st.subheader(f"Modelling {SOURCE_NUM} power plants and wind parks")

for source in sources:
    st.markdown(f"{source['emoji']} **{source['name']}**")
