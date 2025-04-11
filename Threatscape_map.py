import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import pycountry
from datetime import datetime

st.set_page_config(page_title="Threatscape Global Map", layout="wide")
st.title("🌍 Threatscape: Live Global Cyber Threat Map")
st.markdown(
    "This map displays countries reporting high-confidence malicious IP activity, "
    "based on AbuseIPDB's live threat feed."
)

# --- Step 1: AbuseIPDB API Setup ---
API_KEY = "2df847cbf4251df0d253a05c84b3d1ba95e61f7c25a936b97e7b195cb068fee0fe2cea4157b2721f"
headers = {"Key": API_KEY, "Accept": "application/json"}
blacklist_url = "https://api.abuseipdb.com/api/v2/blacklist"

params = {
    "confidenceMinimum": 50,
    "limit": 1000
}

response = requests.get(blacklist_url, headers=headers, params=params)

if response.status_code != 200:
    st.error(f"Failed to fetch data. Status code: {response.status_code}")
    st.text(response.text)
    st.stop()

ips = response.json().get("data", [])

# --- Step 2: Extract country codes from response ---
countries = []
for entry in ips:
    code = entry.get("countryCode")
    if code:
        countries.append(code)

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

# --- Step 4: Plot the map ---
fig = px.choropleth(
    df,
    locations="ISO3",
    color="Incidents",
    hover_name="ISO2",
    color_continuous_scale="YlOrRd",
    projection="natural earth",
    title="Live Threat Reports by Country (AbuseIPDB)"
)

fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# --- Step 5: Add source and timestamp ---
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
st.markdown("---")
st.markdown(
    f"📊 **Data Source:** [AbuseIPDB - IP Blacklist API](https://www.abuseipdb.com/api.html)  \n"
    f"⏱️ **Last updated:** {now}"
)
