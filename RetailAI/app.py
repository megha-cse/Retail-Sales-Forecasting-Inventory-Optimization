
from pathlib import Path
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="RetailAI | Sales & Inventory",
    page_icon="📦",
    layout="wide"
)

# Project folder location
BASE_DIR = Path(__file__).resolve().parent

# File paths
sales_path = BASE_DIR / "data" / "cleaned_sales.csv"
inventory_path = BASE_DIR / "outputs" / "inventory_recommendations.csv"
metrics_path = BASE_DIR / "outputs" / "model_metrics.csv"

# Dashboard heading
st.title("📦 Retail Sales Forecasting & Inventory Optimization")
st.caption("Student portfolio project using a synthetic retail dataset")

# Check required files
required_files = [sales_path, inventory_path]
missing_files = [str(path) for path in required_files if not path.exists()]

if missing_files:
    st.error("Required project files are missing:")
    for file in missing_files:
        st.write(file)
    st.stop()

# Load project data
try:
    sales = pd.read_csv(sales_path, parse_dates=["date"])
    inventory = pd.read_csv(inventory_path)

    metrics = None
    if metrics_path.exists():
        metrics = pd.read_csv(metrics_path).iloc[0]

except Exception as e:
    st.error(f"Error loading project data: {e}")
    st.stop()

# Summary metrics
st.subheader("📊 Business Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Total Units Sold", f"{sales['sales'].sum():,.0f}")
c2.metric("Total Stores", sales["store_id"].nunique())
c3.metric("Total Products", sales["item_id"].nunique())

# Daily sales trend
st.subheader("📈 Daily Sales Trend")

daily = (
    sales.groupby("date", as_index=False)["sales"]
    .sum()
    .set_index("date")
)

st.line_chart(daily)

# Model performance
if metrics is not None:
    st.subheader("🤖 Forecast Model Performance")

    m1, m2, m3 = st.columns(3)

    m1.metric("MAE", f"{metrics['MAE']:.2f}")
    m2.metric("RMSE", f"{metrics['RMSE']:.2f}")
    m3.metric("R² Score", f"{metrics['R2']:.3f}")

# Inventory recommendations
st.subheader("📦 Inventory Recommendations")

st.dataframe(inventory, use_container_width=True)

# Download button
st.download_button(
    label="⬇️ Download Inventory Recommendations CSV",
    data=inventory.to_csv(index=False).encode("utf-8"),
    file_name="inventory_recommendations.csv",
    mime="text/csv"
)

# Project visualizations
st.subheader("📊 Project Visualizations")

image_files = [
    "sales_trend.png",
    "item_sales.png",
    "monthly_sales.png",
    "forecast_comparison.png"
]

for image_file in image_files:
    image_path = BASE_DIR / "outputs" / image_file

    if image_path.exists():
        st.subheader(
            image_file.replace("_", " ").replace(".png", "").title()
        )
        st.image(str(image_path), use_container_width=True)

st.success("RetailAI Dashboard Loaded Successfully!")
