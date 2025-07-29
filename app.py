import streamlit as st
import pandas as pd
def load_assets(path="data_assets.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip() #removes extra spaces from headers
    return df

def save_assets(new_asset, path="data_assets.csv"):
    df = load_assets(path)
    df = pd.concat([df, new_asset], ignore_index=True)
    df.to_csv(path, index=False)
    
from helpers_utils import load_assets, save_assets
from datetime import date

st.set_page_config(page_title="Digital Asset Tracker", layout="wide")

#Title
st.title("🖥️ Digital Asset Tracking System")

#Load Data
assets_df = load_assets(path="data_assets.csv")

#Sidebar Filters
st.sidebar.header("🔍 Filter Assets")
status_filter = st.sidebar.multiselect("Status", options=assets_df["Status"].unique(), default=assets_df["Status"].unique())
location_filter = st. sidebar.multiselect("Location", options=assets_df["Location"].unique(), default=assets_df["Location"].unique())

#Filtered Data
filtered_df = assets_df[(assets_df["Status"].isin(status_filter)) & (assets_df["Location"].isin(location_filter))]

#Display Summary Stats
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Assets", len(assets_df))
col2.metric("In Repair", (assets_df["Status"] == "In Repair").sum())
col3.metric("Expired Warranty", (pd.to_datetime(assets_df["Warranty Expiry"]) < pd.to_datetime(date.today())).sum())

#Asset Table
st.subheader("📋 Asset Inventory")
st.dataframe(filtered_df, use_container_width=True)

#Add New Asset
st.subheader("➕ Add New Asset")
with st.form("new_asset_form"):
    col1, col2 = st.columns(2)
    with col1:
        asset_id = st.text_input("Asset ID")
        name = st.text_input("Asset Name")
        category = st.selectbox("Category", ["Manikin", "Monitor", "Defibrillator", 
                                             "Laptop", "Trainer", "Other"])
        serial = st.text_input("Serial Number")
        location = st.text_input("Location")
    with col2:
        status = st.selectbox("Status", ["Active", "Operational", "In Repair", "Decommissioned"])
        acquisition_date = st.date_input("Acquisition Date")
        vendor = st.text_input("Vendor")
        warranty_expiry = st.date_input("Warranty Expiry")
    
    submit = st.form_submit_button("Add Asset")
    if submit:
        new_row = {
            "Asset ID": asset_id,
            "Asset Name": name,
            "Category": category,
            "Serial Number": serial,
            "Location": location,
            "Status": status,
            "Acquisition Date": acquisition_date,
            "Vendor": vendor,
            "Warranty Expiry": warranty_expiry
        }
        save_assets(pd.DataFrame([new_row]))
        st.success("Asset added successfully! Please refresh to see the update.")
