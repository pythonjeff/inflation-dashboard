import pandas as pd
import matplotlib.pyplot as plt

# Load the inflation data
df = pd.read_csv("data/inflation_data.csv", index_col=0, parse_dates=True)

# Plot inflation trends
def plot_inflation():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["CPI"], label="CPI (Consumer Price Index)", color="blue", linewidth=2)
    plt.plot(df.index, df["Core CPI"], label="Core CPI (Excluding Food & Energy)", color="red", linestyle="dashed")
    plt.plot(df.index, df["PPI"], label="PPI (Producer Price Index)", color="green", linestyle="dotted")

    plt.title("Inflation Trends Over Time")
    plt.xlabel("Year")
    plt.ylabel("Index Value")
    plt.legend()
    plt.grid(True)
    plt.show()

# Calculate and plot moving averages
def plot_moving_averages(short_window=6, long_window=12):
    df["CPI Short MA"] = df["CPI"].rolling(window=short_window).mean()
    df["CPI Long MA"] = df["CPI"].rolling(window=long_window).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["CPI"], label="CPI", color="blue", alpha=0.5)
    plt.plot(df.index, df["CPI Short MA"], label=f"{short_window}-Month MA", color="orange")
    plt.plot(df.index, df["CPI Long MA"], label=f"{long_window}-Month MA", color="red")

    plt.title("CPI with Moving Averages")
    plt.xlabel("Year")
    plt.ylabel("Index Value")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_inflation()
    plot_moving_averages()
