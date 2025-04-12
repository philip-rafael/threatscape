import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import json
from datetime import datetime
import os

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Threatscape Global Map", layout="wide")
st.title("🌍 Global Threatscape: Live Cyber Threat Map")
st.markdown("This map displays countries reporting high-confidence malicious IP activity, based on AbuseIPDB's live threat feed.")

# --- Load cached data ---
DATA_FILE = "cached_threat_data.json"

if not os.path.exists(DATA_FILE):
    st.error("⚠️ No threat data available. Please check back later.")
    st.stop()

with open(DATA_FILE, "r") as f:
    data = json.load(f).get("data", [])

# --- Step 2: Extract country codes ---
countries = [entry.get("countryCode") for entry in data if entry.get("countryCode")]

if not countries:
    st.warning("No country data found in threat feed.")
    st.stop()

# --- Step 3: Process into DataFrame ---
df = pd.Series(countries).value_counts().reset_index()
df.columns = ["ISO2", "Incidents"]

def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

df["ISO3"] = df["ISO2"].apply(iso2_to_iso3)
df = df.dropna()

# --- Step 4: Plot the Map ---
fig = px.choropleth(
    df,
    locations="ISO3",
    color="Incidents",
    hover_name="ISO2",
    color_continuous_scale="YlOrRd",
    projection="natural earth",
    title="Live Threat Reports by Country (AbuseIPDB)"
)

fig.update_layout(margin={"r":0, "t":30, "l":0, "b":0})
st.plotly_chart(fig, use_container_width=True)

# --- Step 5: Footer with timestamp ---
last_updated = datetime.utcfromtimestamp(os.path.getmtime(DATA_FILE)).strftime("%Y-%m-%d %H:%M UTC")
st.markdown("---")
st.markdown(
    f"📊 **Data Source:** [AbuseIPDB - IP Blacklist API](https://www.abuseipdb.com/api.html)  \n"
    f"⏱️ **Last updated:** {last_updated}"
)
