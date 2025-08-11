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