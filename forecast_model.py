import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("TCS_cleaned.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.dropna(subset=["Prev_Close","MA7","MA30","MA50"]).reset_index(drop=True)

FEATURES = ["Open","High","Low","Volume","Prev_Close",
            "Day_of_Week","Month","Quarter","MA7","MA30","Price_Range"]
TARGET = "Close"

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

scaler = MinMaxScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

results = []

lr = LinearRegression()
lr.fit(X_train_sc, y_train)
y_pred_lr = lr.predict(X_test_sc)
results.append({
    "Model" : "Linear Regression",
    "RMSE"  : round(np.sqrt(mean_squared_error(y_test, y_pred_lr)), 4),
    "MAE"   : round(mean_absolute_error(y_test, y_pred_lr), 4),
    "R2"    : round(r2_score(y_test, y_pred_lr), 4)
})
print("Linear Regression done")

rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train_sc, y_train)
y_pred_rf = rf.predict(X_test_sc)
results.append({
    "Model" : "Random Forest",
    "RMSE"  : round(np.sqrt(mean_squared_error(y_test, y_pred_rf)), 4),
    "MAE"   : round(mean_absolute_error(y_test, y_pred_rf), 4),
    "R2"    : round(r2_score(y_test, y_pred_rf), 4)
})
print("Random Forest done")

xgb = XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
xgb.fit(X_train_sc, y_train)
y_pred_xgb = xgb.predict(X_test_sc)
results.append({
    "Model" : "XGBoost",
    "RMSE"  : round(np.sqrt(mean_squared_error(y_test, y_pred_xgb)), 4),
    "MAE"   : round(mean_absolute_error(y_test, y_pred_xgb), 4),
    "R2"    : round(r2_score(y_test, y_pred_xgb), 4)
})
print("XGBoost done")

results_df = pd.DataFrame(results)
results_df.to_csv("tcs_model_results.csv", index=False)
print(results_df)

test_dates = df.loc[X_test.index, "Date"].values
pred_df = pd.DataFrame({
    "Date"           : test_dates,
    "Actual_Close"   : y_test.values,
    "Pred_LR"        : y_pred_lr,
    "Pred_RF"        : y_pred_rf,
    "Pred_XGB"       : y_pred_xgb
}).round(4)
pred_df.to_csv("tcs_predictions.csv", index=False)

feat_imp = pd.DataFrame({
    "Feature"    : FEATURES,
    "RF_Importance"  : rf.feature_importances_,
    "XGB_Importance" : xgb.feature_importances_
}).sort_values("RF_Importance", ascending=False).round(4)
feat_imp.to_csv("tcs_feature_importance.csv", index=False)

print("forecast_model.py done")
print("Output files: tcs_model_results.csv, tcs_predictions.csv, tcs_feature_importance.csv")