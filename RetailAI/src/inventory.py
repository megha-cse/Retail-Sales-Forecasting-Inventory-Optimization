from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from scipy.stats import norm
from src.forecast import add_features, FEATURES

def create_inventory_recommendations(input_path="data/cleaned_sales.csv",
                                     forecast_days=30, lead_time=7):
    df = pd.read_csv(input_path, parse_dates=["date"])
    model = joblib.load("models/retail_forecast_model.pkl")
    rows = []

    for (store, item), history in df.groupby(["store_id", "item_id"]):
        history = history.sort_values("date").copy()
        recent = history.tail(28)
        avg_daily = recent["sales"].mean()
        std_daily = recent["sales"].std(ddof=1)
        if pd.isna(std_daily):
            std_daily = 0.0

        # A simple planning forecast using the latest 28-day average.
        # This makes the inventory policy transparent and reproducible.
        forecast_demand = max(0, avg_daily * forecast_days)
        lead_demand = avg_daily * lead_time
        safety_stock = norm.ppf(0.95) * std_daily * np.sqrt(lead_time)
        reorder_point = lead_demand + safety_stock
        annual_demand = avg_daily * 365
        ordering_cost = 100
        annual_holding_cost_per_unit = max(avg_daily * 0.20, 1)
        eoq = np.sqrt((2 * annual_demand * ordering_cost) / annual_holding_cost_per_unit)

        current_stock = max(0, int(round(avg_daily * 10)))
        recommended_order = max(0, int(np.ceil(reorder_point - current_stock)))
        rows.append({
            "store_id": store,
            "item_id": item,
            "average_daily_sales": round(avg_daily, 2),
            "forecast_30_day_demand": round(forecast_demand, 2),
            "lead_time_days": lead_time,
            "safety_stock": round(safety_stock, 2),
            "reorder_point": round(reorder_point, 2),
            "simulated_current_stock": current_stock,
            "eoq": int(round(eoq)),
            "recommended_order_quantity": recommended_order,
            "action": "REORDER" if current_stock <= reorder_point else "STOCK OK"
        })

    result = pd.DataFrame(rows)
    Path("outputs").mkdir(exist_ok=True)
    result.to_csv("outputs/inventory_recommendations.csv", index=False)
    print("Inventory recommendations saved to outputs/inventory_recommendations.csv")
    return result

if __name__ == "__main__":
    create_inventory_recommendations()
