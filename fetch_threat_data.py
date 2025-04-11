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
    "confidenceMinimum": 10,
    "limit": 1000
}

# --- Fetch data ---
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    with open("cached_threat_data.json", "w") as f:
        json.dump(data, f)
    print(f"✅ Data saved to cached_threat_data.json at {datetime.utcnow().isoformat()} UTC")
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
