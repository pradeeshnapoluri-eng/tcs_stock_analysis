import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("TCS_cleaned.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("=== BASIC STATS ===")
print(df[["Open","High","Low","Close","Volume"]].describe().round(2))

print("=== YEARLY SUMMARY ===")
yearly = df.groupby("Year").agg(
    avg_close    = ("Close",  "mean"),
    max_close    = ("Close",  "max"),
    min_close    = ("Close",  "min"),
    avg_volume   = ("Volume", "mean"),
    total_return = ("Daily_Return", "sum")
).round(2)
print(yearly)
yearly.to_csv("yearly_summary.csv")

print("=== MONTHLY SUMMARY ===")
monthly = df.groupby(["Year","Month","Month_Name"]).agg(
    avg_close  = ("Close",  "mean"),
    max_close  = ("Close",  "max"),
    min_close  = ("Close",  "min"),
    avg_volume = ("Volume", "mean")
).round(2).reset_index()
monthly.to_csv("monthly_summary.csv", index=False)

print("=== QUARTERLY SUMMARY ===")
quarterly = df.groupby(["Year","Quarter"]).agg(
    avg_close  = ("Close",  "mean"),
    max_close  = ("Close",  "max"),
    min_close  = ("Close",  "min"),
    avg_volume = ("Volume", "mean")
).round(2).reset_index()
quarterly.to_csv("quarterly_summary.csv", index=False)

print("=== CORRELATION ===")
corr = df[["Open","High","Low","Close","Volume","Dividends","Stock Splits"]].corr().round(4)
corr.to_csv("correlation_matrix.csv")
print(corr)

print("=== DAILY RETURN STATS ===")
print("Mean daily return:", round(df["Daily_Return"].mean(), 4))
print("Std daily return:",  round(df["Daily_Return"].std(),  4))
print("Max daily return:",  round(df["Daily_Return"].max(),  4))
print("Min daily return:",  round(df["Daily_Return"].min(),  4))

print("=== TOP 10 HIGH CLOSE DAYS ===")
top10 = df.nlargest(10, "Close")[["Date","Open","High","Low","Close","Volume"]]
top10.to_csv("top10_high_close.csv", index=False)
print(top10)

print("=== TOP 10 HIGH VOLUME DAYS ===")
top_vol = df.nlargest(10, "Volume")[["Date","Open","High","Low","Close","Volume"]]
top_vol.to_csv("top10_high_volume.csv", index=False)
print(top_vol)

print("=== DIVIDEND EVENTS ===")
dividends = df[df["Dividends"] > 0][["Date","Close","Dividends"]]
dividends.to_csv("dividend_events.csv", index=False)
print(dividends)

print("eda_analysis.py done")