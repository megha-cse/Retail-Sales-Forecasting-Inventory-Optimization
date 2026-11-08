from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(input_path="data/cleaned_sales.csv"):
    df = pd.read_csv(input_path, parse_dates=["date"])
    Path("outputs").mkdir(exist_ok=True)
    sns.set_theme()

    daily = df.groupby("date", as_index=False)["sales"].sum()
    plt.figure(figsize=(11, 5))
    sns.lineplot(data=daily, x="date", y="sales")
    plt.title("Daily Retail Sales")
    plt.xlabel("Date"); plt.ylabel("Units sold")
    plt.tight_layout()
    plt.savefig("outputs/sales_trend.png", dpi=150)
    plt.close()

    category = df.groupby("item_id", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=category, x="item_id", y="sales")
    plt.title("Total Sales by Item")
    plt.tight_layout()
    plt.savefig("outputs/item_sales.png", dpi=150)
    plt.close()

    monthly = df.assign(month=df["date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["sales"].sum()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="month", y="sales", marker="o")
    plt.xticks(rotation=60)
    plt.title("Monthly Retail Sales")
    plt.tight_layout()
    plt.savefig("outputs/monthly_sales.png", dpi=150)
    plt.close()
    print("EDA charts saved in outputs/")
    return daily

if __name__ == "__main__":
    run_eda()
