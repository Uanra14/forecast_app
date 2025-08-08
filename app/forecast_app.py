import json
import streamlit as st

# Load sources from a JSON file
with open('../data/clean/sources.json', 'r') as f:
    sources = json.load(f)

# Load the results from a JSON file
with open('../outputs/results.json', 'r') as f:
    results = json.load(f)

