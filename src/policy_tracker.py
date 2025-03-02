import os
import pandas as pd
from fredapi import Fred

# Load API Key from environment variable
API_KEY = os.getenv("FRED_API_KEY")

# Define FRED series IDs for key economic indicators
POLICY_SERIES = {
    "Fed Funds Rate": "FEDFUNDS",
    "Unemployment Rate": "UNRATE",
    "30-Year Mortgage Rate": "MORTGAGE30US",
    "Government Surplus/Deficit": "FYFSD",
    "CPI": "CPIAUCSL",
    "MBS Total": "MBST",    
    "Gas Price": "GASREGW",
    "Personal Income": "PI",
    "Personal Consumption Expenditures": "PCE",
    "Total GDP": "GDP",
    "Dow Jones Industrial Average": "DJIA",
    "S&P 500": "SP500",
    "10-Year Treasury Yield": "GS10",
    "3-Month Treasury Yield": "GS3",
    "10-Year Treasury Constant Maturity Rate": "GS10",
    "3-Month Treasury Yield": "GS3",
    "Inflation Rate": "INFLATIONRATE",
}

def fetch_policy_data(series_id, start="2000-01-01"):
    """Fetches data from FRED API."""
    fred = Fred(api_key=API_KEY)
    data = fred.get_series(series_id, start)
    df = pd.DataFrame(data, columns=[series_id])
    df.index = pd.to_datetime(df.index)
    return df

def fetch_all_policy_data():
    """Fetches all selected policy-related datasets from FRED."""
    if not API_KEY:
        raise ValueError("FRED API Key not found! Set it as an environment variable.")

    all_data = []
    for name, series_id in POLICY_SERIES.items():
        df = fetch_policy_data(series_id)
        df.rename(columns={series_id: name}, inplace=True)
        all_data.append(df)

    # Merge into a single DataFrame
    policy_df = pd.concat(all_data, axis=1)

    # Forward-fill missing values so we always have the latest data
    policy_df.ffill(inplace=True)

    # Ensure the data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    policy_df.to_csv("data/policy_data.csv")
    print("✅ Policy data saved successfully!")

if __name__ == "__main__":
    fetch_all_policy_data()
