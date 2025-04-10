import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

st.set_page_config(page_title="Threatscape Global Map", layout="wide")
st.title("🌍 Threatscape: Live Global Cyber Threat Map")
st.markdown("Real-time IP-based threat indicators via AlienVault OTX and geolocation API")

# OTX setup
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual key
headers = {"X-OTX-API-KEY": API_KEY}
url = "https://otx.alienvault.com/api/v1/pulses/subscribed"

# Fetch data
response = requests.get(url, headers=headers)
if response.status_code != 200:
    st.error("Failed to load data from OTX.")
    st.stop()

data = response.json()

# Extract IP indicators only
ip_records = []
for pulse in data["results"]:
    for indicator in pulse["indicators"]:
        if indicator.get("type") == "IPv4":
            ip_records.append(indicator["indicator"])

st.write(f"🔍 Found {len(ip_records)} IPv4 indicators")

# Limit for free IP geolocation API (~45 per min)
max_ips = 40
ip_records = ip_records[:max_ips]

# Geolocate IPs
geo_results = []
for ip in ip_records:
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        if geo["status"] == "success":
            geo_results.append(geo["country"])
        time.sleep(1.5)  # to stay within rate limit
    except:
        pass

# Convert to DataFrame
if geo_results:
    df = pd.Series(geo_results, name="Country").value_counts().reset_index()
    df.columns = ["Country", "Incidents"]

    # Map countries to ISO codes
    import pycountry
    def to_iso(country_name):
        try:
            return pycountry.countries.lookup(country_name).alpha_3
        except:
            return None

    df["ISO_Code"] = df["Country"].apply(to_iso)
    df = df.dropna(subset=["ISO_Code"])

    # Plot
    fig = px.choropleth(
        df,
        locations="ISO_Code",
        color="Incidents",
        hover_name="Country",
        color_continuous_scale="OrRd",
        projection="natural earth",
        title="Live IP-based Threats by Country"
    )

    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No geolocated IPs could be plotted.")
