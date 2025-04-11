import os
import requests
import json
from datetime import datetime

# --- Get API key from environment variable ---
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set in environment variables.")

# --- AbuseIPDB API Setup ---
headers = {"Key": API_KEY, "Accept": "application/json"}
url = "https://api.abuseipdb.com/api/v2/blacklist"
params = {
    "confidenceMinimum": 50,  # <- FIXED: must be between 25–100
    "limit": 1000
}

# --- Fetch data ---
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    filename = "cached_threat_data.json"
    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"✅ Data saved to {filename} at {datetime.utcnow().isoformat()} UTC")
    print("📂 Current working directory:", os.getcwd())
    print("📁 Files in directory:", os.listdir())
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
    print(response.text) 
