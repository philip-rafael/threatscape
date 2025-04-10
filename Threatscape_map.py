import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Threatscape Global Map", layout="wide")
st.title("🌍 Threatscape: Live Global Cyber Threat Map")
st.markdown("Powered by AlienVault OTX")

# Step 1: Pull data from OTX
API_KEY = "baa0dbe2ff9203d251ccd7371644654d4f7e35db45e82e4db64af7663eb975f4"
headers = {"X-OTX-API-KEY": API_KEY}

url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    st.error("Failed to load threat data from OTX")
    st.stop()

data = response.json()

# Step 2: Parse data
records = []
for pulse in data["results"]:
    country = pulse.get("country", "Unknown")
    for indicator in pulse["indicators"]:
        records.append({
            "Country": country,
            "Type": indicator.get("type"),
            "Value": indicator.get("indicator")
        })

df = pd.DataFrame(records)

# Step 3: Count incidents per country
summary = df.groupby("Country").size().reset_index(name="Incidents")

# Optional: Convert country names to ISO codes (simplified demo version)
# For real use: use pycountry or a lookup table
country_iso = {
    "United States": "USA",
    "Germany": "DEU",
    "France": "FRA",
    "United Kingdom": "GBR",
    "India": "IND",
    "Russia": "RUS",
    "Brazil": "BRA",
    "China": "CHN",
    "Unknown": "XXX"
}
summary["ISO_Code"] = summary["Country"].map(country_iso).fillna("XXX")

# Step 4: Plot
fig = px.choropleth(
    summary,
    locations="ISO_Code",
    color="Incidents",
    hover_name="Country",
    color_continuous_scale="Reds",
    projection="natural earth",
    title="Live Cyber Threat Indicators by Country (via OTX)"
)

fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.caption("Data from AlienVault OTX API | Displaying active pulse indicators.")
