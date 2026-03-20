import pandas as pd

# Which standard to keep per pollutant to avoid duplicates
STANDARD_MAP = {
    "PM2.5": "PM25 24-hour 2012",
    "Ozone": "Ozone 8-hour 2015",
    "NO2":   "NO2 Annual 1971",
}

def aqi_category(val, pollutant):
    if pollutant == "PM2.5":
        if val <= 12.0:    return "Good"
        elif val <= 35.4:  return "Moderate"
        elif val <= 55.4:  return "Unhealthy for Sensitive Groups"
        else:              return "Unhealthy"
    elif pollutant == "Ozone":  # ppm
        if val <= 0.054:   return "Good"
        elif val <= 0.070: return "Moderate"
        elif val <= 0.085: return "Unhealthy for Sensitive Groups"
        else:              return "Unhealthy"
    elif pollutant == "NO2":  # ppb
        if val <= 53:      return "Good"
        elif val <= 100:   return "Moderate"
        elif val <= 360:   return "Unhealthy for Sensitive Groups"
        else:              return "Unhealthy"
    return "Unknown"

def clean_pollutant(df, pollutant_name, standard):
    subset = df[
        (df["pollutant_name"] == pollutant_name) &
        (df["pollutant_standard"] == standard)
    ].copy()

    if subset.empty:
        print(f"Warning: no data for {pollutant_name} with standard '{standard}'")
        return pd.DataFrame()

    subset = subset.drop_duplicates(
        subset=["city", "county", "local_site_name", "latitude", "longitude"]
    )

    cols = [
        "pollutant_name",
        "city", "county", "local_site_name", "site_address",
        "latitude", "longitude", "year",
        "arithmetic_mean", "first_max_value", "first_max_datetime",
        "fiftieth_percentile", "ninetieth_percentile",
        "observation_percent", "primary_exceedance_count",
        "units_of_measure",
    ]
    # only keep cols that actually exist in the data
    cols = [c for c in cols if c in subset.columns]
    subset = subset[cols]

    subset = subset.dropna(subset=["arithmetic_mean"])
    subset["aqi_category"] = subset["arithmetic_mean"].apply(
        lambda v: aqi_category(v, pollutant_name)
    )

    return subset

def clean_data():
    raw_df = pd.read_csv("data/raw_all.csv")

    pieces = []
    for pollutant, standard in STANDARD_MAP.items():
        cleaned = clean_pollutant(raw_df, pollutant, standard)
        if not cleaned.empty:
            pieces.append(cleaned)

    df = pd.concat(pieces, ignore_index=True)
    df.to_csv("data/cleaned_all.csv", index=False)
    return df

if __name__ == "__main__":
    df = clean_data()
    print(df.groupby("pollutant_name")[["arithmetic_mean"]].describe())
    print(f"\nTotal rows: {len(df)}")