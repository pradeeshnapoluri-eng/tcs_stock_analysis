import pandas as pd
import sqlite3
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("TCS_cleaned.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

conn = sqlite3.connect("tcs_stock.db")
df.to_sql("tcs_history", conn, if_exists="replace", index=False)
print("Data loaded into tcs_stock.db")

queries = {
    "sql_overall_stats"    : "SELECT COUNT(*) AS total_trading_days, ROUND(MIN(Close),2) AS all_time_low, ROUND(MAX(Close),2) AS all_time_high, ROUND(AVG(Close),2) AS avg_close, ROUND(AVG(Volume),2) AS avg_volume FROM tcs_history",
    "sql_yearly_stats"     : "SELECT Year, ROUND(AVG(Close),2) AS avg_close, ROUND(MAX(Close),2) AS yearly_high, ROUND(MIN(Close),2) AS yearly_low, ROUND(AVG(Volume),2) AS avg_volume FROM tcs_history GROUP BY Year ORDER BY Year",
    "sql_monthly_stats"    : "SELECT Year, Month, Month_Name, ROUND(AVG(Close),2) AS avg_close, ROUND(MAX(Close),2) AS month_high, ROUND(MIN(Close),2) AS month_low FROM tcs_history GROUP BY Year, Month ORDER BY Year, Month",
    "sql_quarterly_stats"  : "SELECT Year, Quarter, ROUND(AVG(Close),2) AS avg_close, ROUND(MAX(Close),2) AS quarter_high, ROUND(MIN(Close),2) AS quarter_low FROM tcs_history GROUP BY Year, Quarter ORDER BY Year, Quarter",
    "sql_top10_high"       : "SELECT Date, ROUND(Open,2) AS Open, ROUND(High,2) AS High, ROUND(Low,2) AS Low, ROUND(Close,2) AS Close, Volume FROM tcs_history ORDER BY Close DESC LIMIT 10",
    "sql_top10_volume"     : "SELECT Date, ROUND(Close,2) AS Close, Volume FROM tcs_history ORDER BY Volume DESC LIMIT 10",
    "sql_dividends"        : "SELECT Date, ROUND(Close,2) AS Close, ROUND(Dividends,2) AS Dividends FROM tcs_history WHERE Dividends > 0 ORDER BY Date",
    "sql_day_of_week"      : "SELECT Day_of_Week, ROUND(AVG(Daily_Return),4) AS avg_return, COUNT(*) AS trading_days FROM tcs_history GROUP BY Day_of_Week ORDER BY avg_return DESC",
    "sql_best_months"      : "SELECT Month_Name, ROUND(AVG(Daily_Return),4) AS avg_daily_return, COUNT(*) AS trading_days FROM tcs_history GROUP BY Month_Name ORDER BY avg_daily_return DESC",
    "sql_price_bands"      : "SELECT CASE WHEN Close >= 3500 THEN 'Above 3500' WHEN Close >= 3000 THEN '3000-3500' WHEN Close >= 2000 THEN '2000-3000' WHEN Close >= 1000 THEN '1000-2000' WHEN Close >= 500 THEN '500-1000' ELSE 'Below 500' END AS price_band, COUNT(*) AS trading_days FROM tcs_history GROUP BY price_band",
    "sql_signals"          : "SELECT Year, SUM(CASE WHEN Signal=1 THEN 1 ELSE 0 END) AS buy_days, SUM(CASE WHEN Signal=-1 THEN 1 ELSE 0 END) AS sell_days FROM tcs_history GROUP BY Year ORDER BY Year",
    "sql_recent30"         : "SELECT Date, ROUND(Open,2) AS Open, ROUND(High,2) AS High, ROUND(Low,2) AS Low, ROUND(Close,2) AS Close, Volume, ROUND(MA7,2) AS MA7, ROUND(MA30,2) AS MA30 FROM tcs_history ORDER BY Date DESC LIMIT 30"
}

for name, query in queries.items():
    try:
        result = pd.read_sql_query(query, conn)
        result.to_csv(name + ".csv", index=False)
        print("Saved:", name + ".csv", "—", len(result), "rows")
    except Exception as e:
        print("Error in", name, ":", e)

conn.close()
print("execute_sql.py done — tcs_stock.db created")