import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
import pycountry

st.set_page_config(page_title="Threatscape Global Map", layout="wide")
st.title("🌍 Threatscape: Live Global Cyber Threat Map")
st.markdown("Real-time IP-based threat indicators via AlienVault OTX and geolocation API")

# --- Step 1: Get list of recent IPv4 indicators from OTX bulk export ---
export_url = "https://otx.alienvault.com/api/v1/indicators/export?type=IPv4"

response = requests.get(export_url)

if response.status_code != 200:
    st.error(f"Failed to load IPv4 data. Status code: {response.status_code}")
    st.text(response.text)
    st.stop()


# Parse IPs from plain text response
ip_list = response.text.strip().split("\n")

st.write(f"🔍 Fetched {len(ip_list)} IPv4 indicators from OTX")

# --- Step 2: Limit for rate-limited geolocation ---
max_ips = 40
ip_records = ip_list[:max_ips]

# --- Step 3: Geolocate each IP using ip-api.com ---
geo_results = []
for ip in ip_records:
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        if geo["status"] == "success":
            geo_results.append(geo["country"])
        time.sleep(1.5)  # Respect free rate limit (~45 requests/min)
    except:
        pass

# --- Step 4: Summarise and plot ---
if geo_results:
    df = pd.Series(geo_results, name="Country").value_counts().reset_index()
    df.columns = ["Country", "Incidents"]

    def to_iso(country_name):
        try:
            return pycountry.countries.lookup(country_name).alpha_3
        except:
            return None

    df["ISO_Code"] = df["Country"].apply(to_iso)
    df = df.dropna(subset=["ISO_Code"])

    # Choropleth
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
    st.warning("No IPs could be geolocated. Try refreshing later.")
