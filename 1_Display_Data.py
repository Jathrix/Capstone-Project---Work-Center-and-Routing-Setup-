# 1_Display_Data.py
import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path

st.title("📊 Display Work Center & Routing Data")

# Path to json folder
json_folder = Path(__file__).parent / "json"
json_folder.mkdir(exist_ok=True)

# User inputs filename
file_name = st.text_input("Enter the JSON file name (without .json):")

if file_name:
    file_path = json_folder / f"{file_name}.json"

    if file_path.exists():
        st.success(f"✅ Found file: {file_path.name}")

        # Load JSON
        with open(file_path, "r") as f:
            data = json.load(f)

        # Convert to DataFrames
        work_centers_df = pd.DataFrame(data.get("work_centers", []))
        routing_df = pd.DataFrame(data.get("routing", []))
        quantity = data.get("quantity", None)

        # Display Work Centers
        st.subheader("🏭 Work Centers")
        if not work_centers_df.empty:
            st.dataframe(work_centers_df)
        else:
            st.info("No work center data found.")

        # Display Routing
        st.subheader("🔄 Routing Steps")
        if not routing_df.empty:
            st.dataframe(routing_df)
        else:
            st.info("No routing data found.")

        # Display Quantity
        st.subheader("📦 Production Quantity")
        st.write(quantity)

        # Example: summary using numpy
        if not work_centers_df.empty:
            try:
                costs = np.array(work_centers_df["cost_per_hour"], dtype=float)
                st.subheader("📈 Summary Stats")
                st.write(f"Total Cost/hr: {np.sum(costs)}")
                st.write(f"Average Cost/hr: {np.mean(costs):.2f}")
            except Exception:
                st.warning("⚠️ Could not compute stats, check data types.")
    else:
        st.error(f"❌ File '{file_name}.json' not found in {json_folder}")
