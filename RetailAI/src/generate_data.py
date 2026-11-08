from pathlib import Path
import numpy as np
import pandas as pd

def generate_data():
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    stores = ["Store_1", "Store_2"]
    items = [f"SKU_{i:02d}" for i in range(1, 9)]
    rows = []

    for store in stores:
        for item in items:
            base = np.random.randint(15, 55)
            for date in dates:
                annual = 1 + 0.20 * np.sin(2 * np.pi * date.dayofyear / 365.25)
                weekend = 1.15 if date.dayofweek >= 5 else 1.0
                promotion = int(np.random.random() < 0.15)
                trend = 1 + (date - dates[0]).days / len(dates) * 0.08
                demand = base * annual * weekend * (1.35 if promotion else 1) * trend
                sales = max(0, int(np.random.normal(demand, 5)))
                rows.append({
                    "date": date, "store_id": store, "item_id": item,
                    "sales": sales, "promotion": promotion, "stockout": 0
                })

    df = pd.DataFrame(rows)
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/retail_sales.csv", index=False)
    print(f"Created data/retail_sales.csv ({len(df):,} rows)")
    return df

if __name__ == "__main__":
    generate_data()
