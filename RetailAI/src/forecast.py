from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURES = ["day_of_week", "day_of_year", "month", "promotion",
            "lag_1", "lag_7", "rolling_7", "rolling_28"]

def add_features(group):
    group = group.sort_values("date").copy()
    group["day_of_week"] = group["date"].dt.dayofweek
    group["day_of_year"] = group["date"].dt.dayofyear
    group["month"] = group["date"].dt.month
    group["lag_1"] = group["sales"].shift(1)
    group["lag_7"] = group["sales"].shift(7)
    group["rolling_7"] = group["sales"].shift(1).rolling(7).mean()
    group["rolling_28"] = group["sales"].shift(1).rolling(28).mean()
    return group

def train_model(input_path="data/cleaned_sales.csv"):
    df = pd.read_csv(input_path, parse_dates=["date"])
    featured = []
    for _, group in df.groupby(["store_id", "item_id"]):
        featured.append(add_features(group))
    data = pd.concat(featured).dropna().sort_values("date")

    cutoff = data["date"].max() - pd.Timedelta(days=59)
    train = data[data["date"] <= cutoff]
    test = data[data["date"] > cutoff]

    model = RandomForestRegressor(
        n_estimators=120, max_depth=12, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    )
    model.fit(train[FEATURES], train["sales"])
    predictions = np.maximum(0, model.predict(test[FEATURES]))

    mae = mean_absolute_error(test["sales"], predictions)
    rmse = np.sqrt(mean_squared_error(test["sales"], predictions))
    r2 = r2_score(test["sales"], predictions)

    Path("models").mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)
    joblib.dump(model, "models/retail_forecast_model.pkl")

    comparison = test[["date", "sales"]].copy()
    comparison["predicted_sales"] = predictions
    comparison.to_csv("outputs/test_predictions.csv", index=False)

    plot_data = comparison.groupby("date")[["sales", "predicted_sales"]].sum()
    plt.figure(figsize=(11, 5))
    plt.plot(plot_data.index, plot_data["sales"], label="Actual")
    plt.plot(plot_data.index, plot_data["predicted_sales"], label="Predicted")
    plt.title("Actual vs Predicted Sales (Test Period)")
    plt.xlabel("Date"); plt.ylabel("Units sold"); plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/forecast_comparison.png", dpi=150)
    plt.close()

    metrics = {"MAE": mae, "RMSE": rmse, "R2": r2}
    pd.DataFrame([metrics]).to_csv("outputs/model_metrics.csv", index=False)
    print("Model trained and saved.")
    print(f"MAE: {mae:.2f} | RMSE: {rmse:.2f} | R2: {r2:.3f}")
    return metrics

if __name__ == "__main__":
    train_model()
