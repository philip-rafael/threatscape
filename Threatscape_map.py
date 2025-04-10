import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import pycountry

st.set_page_config(page_title="Threatscape Global Map", layout="wide")
st.title("🌍 Threatscape: Live Global Cyber Threat Map")
st.markdown("Real-time threat reports from AbuseIPDB")

# --- Step 1: AbuseIPDB API Setup ---
API_KEY = "caea84e481aaf415314e925ab7e083aa8f863a104258f8695829cdf892f3ed0c2bc5f1f5bb54965f"
headers = {"Key": API_KEY, "Accept": "application/json"}
url = "https://api.abuseipdb.com/api/v2/reports"

# --- Step 2: Fetch recent reports (you can use a sample IP to pull multiple) ---
params = {
    "ipAddress": "1.1.1.1",  # abuseIPDB uses an IP input to return recent report patterns
    "maxAgeInDays": 30,
    "verbose": True
}

response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    st.error(f"Failed to fetch data. Status code: {response.status_code}")
    st.text(response.text)
    st.stop()

data = response.json()

# --- Step 3: Parse country data from response ---
# abuseIPDB returns only reports for a given IP, so for now we use the blacklist endpoint instead
# Instead, we'll switch to a better AbuseIPDB endpoint for broader data:
blacklist_url = "https://api.abuseipdb.com/api/v2/blacklist"
params = {
    "confidenceMinimum": 50,
    "limit": 1000
}
response = requests.get(blacklist_url, headers=headers, params=params)

if response.status_code != 200:
    st.error("Failed to load IP blacklist.")
    st.text(response.text)
    st.stop()

ips = response.json().get("data", [])

# --- Step 4: Extract country data from IP metadata ---
countries = []
for entry in ips:
    country = entry.get("countryCode")
    if country:
        countries.append(country)

if not countries:
    st.warning("No country data found in threat feed.")
    st.stop()

# --- Step 5: Convert to DataFrame, map ISO2 to ISO3, and count ---
country_counts = pd.Series(countries).value_counts().reset_index()
country_counts.columns = ["ISO2", "Incidents"]

def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

country_counts["ISO3"] = country_counts["ISO2"].apply(iso2_to_iso3)
country_counts = country_counts.dropna()

# --- Step 6: Plot Choropleth Map ---
fig = px.choropleth(
    country_counts,
    locations="ISO3",
    color="Incidents",
    hover_name="ISO2",
    color_continuous_scale="YlOrRd",
    title="Live Threat Reports by Country (AbuseIPDB)"
)

fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)
