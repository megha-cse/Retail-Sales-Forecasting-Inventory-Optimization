from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="RetailAI | Sales & Inventory", page_icon="📦", layout="wide")
st.title("📦 Retail Sales Forecasting & Inventory Optimization")
st.caption("Student portfolio project using a synthetic retail dataset")

sales_path = Path("data/cleaned_sales.csv")
inventory_path = Path("outputs/inventory_recommendations.csv")
metrics_path = Path("outputs/model_metrics.csv")

if not sales_path.exists() or not inventory_path.exists():
    st.warning("Project outputs are not ready yet. Run `python run_pipeline.py` in the terminal first.")
    st.stop()

sales = pd.read_csv(sales_path, parse_dates=["date"])
inventory = pd.read_csv(inventory_path)
metrics = pd.read_csv(metrics_path).iloc[0] if metrics_path.exists() else None

c1, c2, c3 = st.columns(3)
c1.metric("Total units sold", f"{sales['sales'].sum():,}")
c2.metric("Stores", sales["store_id"].nunique())
c3.metric("Products", sales["item_id"].nunique())

st.subheader("Daily sales trend")
daily = sales.groupby("date", as_index=False)["sales"].sum().set_index("date")
st.line_chart(daily)

if metrics is not None:
    st.subheader("Forecast model performance")
    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{metrics['MAE']:.2f}")
    m2.metric("RMSE", f"{metrics['RMSE']:.2f}")
    m3.metric("R²", f"{metrics['R2']:.3f}")

st.subheader("Inventory recommendations")
st.dataframe(inventory, use_container_width=True)
st.download_button(
    "Download inventory recommendations CSV",
    inventory.to_csv(index=False).encode("utf-8"),
    file_name="inventory_recommendations.csv",
    mime="text/csv"
)

for image_file in ["sales_trend.png", "item_sales.png", "monthly_sales.png", "forecast_comparison.png"]:
    image_path = Path("outputs") / image_file
    if image_path.exists():
        st.subheader(image_file.replace("_", " ").replace(".png", "").title())
        st.image(str(image_path), use_container_width=True)
