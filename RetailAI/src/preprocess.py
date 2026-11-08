from pathlib import Path
import pandas as pd

def preprocess_data(input_path="data/retail_sales.csv",
                    output_path="data/cleaned_sales.csv"):
    df = pd.read_csv(input_path, parse_dates=["date"])
    required = ["date", "store_id", "item_id", "sales", "promotion", "stockout"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.drop_duplicates()
    df = df.dropna(subset=required)
    df = df[df["sales"] >= 0]
    df = df[df["stockout"] == 0].copy()
    df = df.sort_values(["store_id", "item_id", "date"])
    Path("data").mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path} ({len(df):,} rows)")
    return df

if __name__ == "__main__":
    preprocess_data()
