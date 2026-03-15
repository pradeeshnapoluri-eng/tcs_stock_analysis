import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("TCS_cleaned.csv")
df["Date"] = pd.to_datetime(df["Date"])

sns.set_style("darkgrid")
plt.rcParams["figure.dpi"] = 150

print("Building charts...")

plt.figure(figsize=(14, 6))
plt.plot(df["Date"], df["Close"], color="#1565c0", linewidth=1.2, label="Close Price")
plt.title("TCS Stock Close Price Over Time")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.tight_layout()
plt.savefig("chart_close_price.png")
plt.close()

plt.figure(figsize=(14, 6))
plt.plot(df["Date"], df["Close"],  color="#1565c0", linewidth=1,   label="Close")
plt.plot(df["Date"], df["MA30"],   color="#e53935", linewidth=1.5, label="MA30")
plt.plot(df["Date"], df["MA50"],   color="#43a047", linewidth=1.5, label="MA50")
plt.plot(df["Date"], df["MA200"],  color="#fb8c00", linewidth=2,   label="MA200")
plt.title("TCS Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.tight_layout()
plt.savefig("chart_moving_averages.png")
plt.close()

plt.figure(figsize=(14, 4))
plt.bar(df["Date"], df["Volume"], color="#1565c0", alpha=0.6, width=1)
plt.title("TCS Trading Volume Over Time")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.tight_layout()
plt.savefig("chart_volume.png")
plt.close()

plt.figure(figsize=(8, 6))
df["Daily_Return"].dropna().hist(bins=80, color="#1565c0", alpha=0.7, edgecolor="white")
plt.title("Distribution of Daily Returns")
plt.xlabel("Daily Return %")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("chart_daily_returns.png")
plt.close()

yearly = df.groupby("Year")["Close"].mean().reset_index()
plt.figure(figsize=(12, 5))
plt.bar(yearly["Year"], yearly["Close"], color="#1565c0", alpha=0.8)
plt.title("Average Close Price by Year")
plt.xlabel("Year")
plt.ylabel("Avg Close Price (INR)")
plt.tight_layout()
plt.savefig("chart_yearly_avg.png")
plt.close()

corr = df[["Open","High","Low","Close","Volume","Dividends"]].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("chart_correlation.png")
plt.close()

plt.figure(figsize=(14, 5))
plt.plot(df["Date"], df["Volatility_30"], color="#e53935", linewidth=1)
plt.title("30-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility (%)")
plt.tight_layout()
plt.savefig("chart_volatility.png")
plt.close()

print("chart_builder.py done — 7 charts saved")