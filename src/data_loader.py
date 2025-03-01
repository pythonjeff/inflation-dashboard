import os
import pandas as pd
from fredapi import Fred

# Load API Key from environment variable
API_KEY = os.getenv("FRED_API_KEY")

# Define FRED series IDs for inflation-related data
INFLATION_SERIES = {
    "CPI": "CPIAUCSL",  # Consumer Price Index (All Urban Consumers)
    "Core CPI": "CPILFESL",  # Core CPI (Excluding Food and Energy)
    "PPI": "PPIACO",  # Producer Price Index (All Commodities)
}



def fetch_fred_data(series_id, start="2000-01-01"):
    """Fetches inflation-related data from FRED API."""
    fred = Fred(api_key=API_KEY)
    data = fred.get_series(series_id, start)
    df = pd.DataFrame(data, columns=[series_id])
    df.index = pd.to_datetime(df.index)
    return df

def fetch_all_inflation_data():
    """Fetches multiple inflation-related datasets from FRED."""
    if not API_KEY:
        raise ValueError("FRED API Key not found! Set it as an environment variable.")

    all_data = []
    for name, series_id in INFLATION_SERIES.items():
        df = fetch_fred_data(series_id)
        df.rename(columns={series_id: name}, inplace=True)
        all_data.append(df)

    # Merge all data into a single DataFrame
    inflation_df = pd.concat(all_data, axis=1)
    inflation_df.to_csv("data/inflation_data.csv")
    print("Inflation data saved successfully!")

if __name__ == "__main__":
    fetch_all_inflation_data()
