import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("TCS_stock_history.csv")

df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

df["Open"]   = pd.to_numeric(df["Open"],   errors="coerce")
df["High"]   = pd.to_numeric(df["High"],   errors="coerce")
df["Low"]    = pd.to_numeric(df["Low"],    errors="coerce")
df["Close"]  = pd.to_numeric(df["Close"],  errors="coerce")
df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")

df["Dividends"]    = pd.to_numeric(df["Dividends"],    errors="coerce").fillna(0)
df["Stock Splits"] = pd.to_numeric(df["Stock Splits"], errors="coerce").fillna(0)

df = df.ffill().dropna(subset=["Open","High","Low","Close"])
df = df.drop_duplicates(subset=["Date"]).reset_index(drop=True)

df["Year"]             = df["Date"].dt.year
df["Month"]            = df["Date"].dt.month
df["Day"]              = df["Date"].dt.day
df["Day_of_Week"]      = df["Date"].dt.dayofweek
df["Month_Name"]       = df["Date"].dt.strftime("%B")
df["Quarter"]          = df["Date"].dt.quarter

df["Daily_Return"]     = df["Close"].pct_change() * 100
df["Price_Range"]      = df["High"] - df["Low"]
df["Prev_Close"]       = df["Close"].shift(1)
df["MA7"]              = df["Close"].rolling(window=7).mean()
df["MA30"]             = df["Close"].rolling(window=30).mean()
df["MA50"]             = df["Close"].rolling(window=50).mean()
df["MA200"]            = df["Close"].rolling(window=200).mean()
df["Volatility_30"]    = df["Daily_Return"].rolling(window=30).std()
df["Short_MA"]         = df["Close"].rolling(window=5).mean()
df["Long_MA"]          = df["Close"].rolling(window=30).mean()
df["Signal"]           = np.where(df["Short_MA"] > df["Long_MA"], 1, -1)

df.to_csv("TCS_cleaned.csv", index=False)
print("preprocess.py done")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Date range:", df["Date"].min(), "to", df["Date"].max())