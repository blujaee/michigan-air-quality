import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EPA_EMAIL")
KEY = os.getenv("EPA_KEY")
BASE_URL = "https://aqs.epa.gov/data/api"

POLLUTANTS = {
    "PM2.5": "88101",
    "Ozone": "44201",
    "NO2": "42602",
}


def get_annual_summary(param,bdate,edate,state):
    url = f"{BASE_URL}/annualData/byState?"
    params = {"email": EMAIL, "key": KEY, "param": param, "bdate": bdate, "edate": edate, "state": state}
    resp = requests.get(url, params = params)
    data = resp.json().get("Data", [])
    if not data:
        print(f"No data returned for param {param}")
        return pd.DataFrame()
    df = pd.DataFrame.from_dict(data)
    return df

if __name__ == "__main__":
    all_dfs = []

    for name, param in POLLUTANTS.items():
        print(f"Fetching {name} ({param})...")
        df = get_annual_summary(param, "20240101", "20241231", "26")
        if not df.empty:
            df["pollutant_name"] = name
            all_dfs.append(df)

    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_csv("data/raw_all.csv", index=False)
    print(f"Saved {len(combined)} rows to data/raw_all.csv")

