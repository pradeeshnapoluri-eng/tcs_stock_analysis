from flask import send_file
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)

HISTORY_CSV    = "TCS_cleaned.csv"
ML_RESULTS_CSV = "tcs_model_results.csv"
PRED_CSV       = "tcs_predictions.csv"
FEAT_CSV       = "tcs_feature_importance.csv"

def load_history():
    df = pd.read_csv(HISTORY_CSV)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

@app.route("/")
def index():
    return render_template("tcs_dashboard.html")

@app.route("/charts/<filename>")
def serve_chart(filename):
    filepath=os.path.join(os.getcwd(),filename)
    return send_file(filename, mimetype="image/png")

@app.route("/api/tcs/summary")
def tcs_summary():
    try:
        df = load_history()
        latest = df.iloc[-1]
        prev   = df.iloc[-2]
        change = round(float(latest["Close"]) - float(prev["Close"]), 2)
        change_pct = round((change / float(prev["Close"])) * 100, 2)
        return jsonify({
            "total_days"       : int(len(df)),
            "all_time_high"    : round(float(df["High"].max()),    2),
            "all_time_low"     : round(float(df["Low"].min()),     2),
            "latest_close"     : round(float(latest["Close"]),     2),
            "latest_open"      : round(float(latest["Open"]),      2),
            "latest_high"      : round(float(latest["High"]),      2),
            "latest_low"       : round(float(latest["Low"]),       2),
            "latest_volume"    : int(latest["Volume"]),
            "latest_date"      : str(latest["Date"].date()),
            "day_change"       : change,
            "day_change_pct"   : change_pct,
            "avg_close"        : round(float(df["Close"].mean()),  2),
            "avg_volume"       : round(float(df["Volume"].mean()), 2),
            "total_dividends"  : round(float(df["Dividends"].sum()), 2),
            "date_from"        : str(df["Date"].min().date()),
            "date_to"          : str(df["Date"].max().date())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/price_history")
def price_history():
    try:
        df = load_history()
        df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
        return jsonify({
            "dates"  : df["DateStr"].tolist(),
            "open"   : df["Open"].round(2).tolist(),
            "high"   : df["High"].round(2).tolist(),
            "low"    : df["Low"].round(2).tolist(),
            "close"  : df["Close"].round(2).tolist(),
            "volume" : df["Volume"].tolist(),
            "ma7"    : df["MA7"].round(2).tolist(),
            "ma30"   : df["MA30"].round(2).tolist(),
            "ma50"   : df["MA50"].round(2).tolist(),
            "ma200"  : df["MA200"].round(2).tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/yearly")
def yearly():
    try:
        df = load_history()
        result = df.groupby("Year").agg(
            avg_close  = ("Close",  "mean"),
            max_close  = ("Close",  "max"),
            min_close  = ("Close",  "min"),
            avg_volume = ("Volume", "mean"),
            avg_return = ("Daily_Return", "mean")
        ).round(2).reset_index()
        result["Year"] = result["Year"].astype(int)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/monthly")
def monthly():
    try:
        df = load_history()
        result = df.groupby(["Year","Month","Month_Name"]).agg(
            avg_close  = ("Close",  "mean"),
            max_close  = ("Close",  "max"),
            min_close  = ("Close",  "min"),
            avg_volume = ("Volume", "mean")
        ).round(2).reset_index()
        result["Year"]  = result["Year"].astype(int)
        result["Month"] = result["Month"].astype(int)
        result = result.sort_values(["Year","Month"])
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/quarterly")
def quarterly():
    try:
        df = load_history()
        result = df.groupby(["Year","Quarter"]).agg(
            avg_close  = ("Close",  "mean"),
            max_close  = ("Close",  "max"),
            min_close  = ("Close",  "min"),
            avg_volume = ("Volume", "mean")
        ).round(2).reset_index()
        result["Year"]    = result["Year"].astype(int)
        result["Quarter"] = result["Quarter"].astype(int)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/moving_averages")
def moving_averages():
    try:
        df = load_history()
        recent = df.tail(500).copy()
        recent["DateStr"] = recent["Date"].dt.strftime("%Y-%m-%d")
        return jsonify({
            "dates" : recent["DateStr"].tolist(),
            "close" : recent["Close"].round(2).tolist(),
            "ma7"   : recent["MA7"].round(2).tolist(),
            "ma30"  : recent["MA30"].round(2).tolist(),
            "ma50"  : recent["MA50"].round(2).tolist(),
            "ma200" : recent["MA200"].round(2).tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/volatility")
def volatility():
    try:
        df = load_history()
        result = df.groupby("Year").agg(
            avg_volatility = ("Volatility_30", "mean"),
            max_volatility = ("Volatility_30", "max")
        ).round(4).reset_index()
        result["Year"] = result["Year"].astype(int)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/daily_returns")
def daily_returns():
    try:
        df = load_history()
        result = df.groupby("Year").agg(
            avg_return   = ("Daily_Return", "mean"),
            total_return = ("Daily_Return", "sum"),
            positive_days = ("Daily_Return", lambda x: (x > 0).sum()),
            negative_days = ("Daily_Return", lambda x: (x < 0).sum())
        ).round(4).reset_index()
        result["Year"] = result["Year"].astype(int)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/signals")
def signals():
    try:
        df = load_history()
        result = df.groupby("Year").agg(
            buy_days  = ("Signal", lambda x: (x ==  1).sum()),
            sell_days = ("Signal", lambda x: (x == -1).sum())
        ).reset_index()
        result["Year"] = result["Year"].astype(int)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/price_bands")
def price_bands():
    try:
        df = load_history()
        bins   = [0, 500, 1000, 2000, 3000, 3500, float("inf")]
        labels = ["Below 500","500-1000","1000-2000","2000-3000","3000-3500","Above 3500"]
        df["band"] = pd.cut(df["Close"], bins=bins, labels=labels)
        result = df.groupby("band", observed=True).size().reset_index(name="trading_days")
        result.columns = ["price_band","trading_days"]
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/top10_high")
def top10_high():
    try:
        df = load_history()
        df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
        result = df.nlargest(10, "Close")[["DateStr","Open","High","Low","Close","Volume"]]
        result.columns = ["Date","Open","High","Low","Close","Volume"]
        return jsonify(result.round(2).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/top10_volume")
def top10_volume():
    try:
        df = load_history()
        df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
        result = df.nlargest(10, "Volume")[["DateStr","Open","High","Low","Close","Volume"]]
        result.columns = ["Date","Open","High","Low","Close","Volume"]
        return jsonify(result.round(2).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/dividends")
def dividends():
    try:
        df = load_history()
        df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
        result = df[df["Dividends"] > 0][["DateStr","Close","Dividends"]]
        result.columns = ["Date","Close","Dividends"]
        return jsonify(result.round(2).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/recent30")
def recent30():
    try:
        df = load_history()
        df["DateStr"] = df["Date"].dt.strftime("%Y-%m-%d")
        result = df.tail(30)[["DateStr","Open","High","Low","Close","Volume","MA7","MA30","Daily_Return"]]
        result.columns = ["Date","Open","High","Low","Close","Volume","MA7","MA30","Daily_Return"]
        return jsonify(result.round(2).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/ml_results")
def ml_results():
    try:
        if not os.path.exists(ML_RESULTS_CSV):
            return jsonify({"error": "tcs_model_results.csv not found — run forecast_model.py first"}), 404
        df = pd.read_csv(ML_RESULTS_CSV)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/predictions")
def predictions():
    try:
        if not os.path.exists(PRED_CSV):
            return jsonify({"error": "tcs_predictions.csv not found"}), 404
        df = pd.read_csv(PRED_CSV)
        df = df.tail(200)
        return jsonify({
            "dates"    : df["Date"].tolist(),
            "actual"   : df["Actual_Close"].round(2).tolist(),
            "pred_lr"  : df["Pred_LR"].round(2).tolist(),
            "pred_rf"  : df["Pred_RF"].round(2).tolist(),
            "pred_xgb" : df["Pred_XGB"].round(2).tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/feature_importance")
def feature_importance():
    try:
        if not os.path.exists(FEAT_CSV):
            return jsonify({"error": "tcs_feature_importance.csv not found"}), 404
        df = pd.read_csv(FEAT_CSV)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tcs/best_months")
def best_months():
    try:
        df = load_history()
        result = df.groupby("Month_Name").agg(
            avg_return    = ("Daily_Return", "mean"),
            trading_days  = ("Daily_Return", "count"),
            avg_close     = ("Close", "mean")
        ).round(4).reset_index()
        result = result.sort_values("avg_return", ascending=False)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Checking files...")
    for f in [HISTORY_CSV, ML_RESULTS_CSV, PRED_CSV, FEAT_CSV]:
        status = "OK" if os.path.exists(f) else "MISSING — run scripts first"
        print(f, ":", status)
    print("Starting TCS dashboard on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
