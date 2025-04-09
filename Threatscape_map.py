import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Threatscape World Map", layout="wide")
st.title("🌍 Threatscape: Global Cyber Threat Map")
st.markdown("Visualising cybersecurity threat incidents by country.")

# Example data — you can replace with real stats
data = {
    "Country": ["Germany", "France", "Italy", "Spain", "United Kingdom", "Netherlands"],
    "ISO_Code": ["DEU", "FRA", "ITA", "ESP", "GBR", "NLD"],
    "Incidents": [22, 18, 12, 9, 25, 14]
}

df = pd.DataFrame(data)

# Choropleth map
fig = px.choropleth(
    df,
    locations="ISO_Code",
    color="Incidents",
    hover_name="Country",
    color_continuous_scale="Reds",
    projection="natural earth",
    title="Cybersecurity Threat Incidents by Country"
)

fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

st.markdown("**Data source:** Demo data. Replace with live threat intel for real-time mapping.")
