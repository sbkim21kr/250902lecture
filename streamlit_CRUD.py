import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/items/"

st.title("📦 FastAPI + Streamlit Item Manager")

# --- Create Item ---
st.header("✅ Create Item")
name = st.text_input("Name")
description = st.text_input("Description")
price = st.number_input("Price", min_value=0)
tax = st.number_input("Tax", min_value=0)

if st.button("Create"):
    item = {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax
    }
    res = requests.post(API_URL, json=item)
    if res.status_code == 201:
        st.success(f"Item created: {res.json()}")
    else:
        st.error(f"Error: {res.text}")

# --- Read All Items ---
st.header("📋 Read All Items")
if st.button("Load All Items"):
    res = requests.get(API_URL)
    if res.status_code == 200:
        items = res.json()
        if items:
            df = pd.DataFrame(items)
            st.dataframe(df)
        else:
            st.info("No items found.")
    else:
        st.error("Failed to load items")

# --- Read One Item ---
st.header("🔍 Read One Item")
read_id = st.number_input("Enter Item ID to Read", min_value=1, step=1)
if st.button("Read Item"):
    res = requests.get(f"{API_URL}{int(read_id)}")
    if res.status_code == 200:
        st.json(res.json())
    else:
        st.error("Item not found")

# --- Update Item ---
st.header("✏️ Update Item")
update_id = st.number_input("Enter Item ID to Update", min_value=1, step=1)

with st.expander("Enter New Item Data"):
    new_name = st.text_input("New Name", key="update_name")
    new_description = st.text_input("New Description", key="update_description")
    new_price = st.number_input("New Price", min_value=0, key="update_price")
    new_tax = st.number_input("New Tax", min_value=0, key="update_tax")

if st.button("Update Item"):
    updated_item = {
        "name": new_name,
        "description": new_description,
        "price": new_price,
        "tax": new_tax
    }
    res = requests.put(f"{API_URL}{int(update_id)}", json=updated_item)
    if res.status_code == 200:
        st.success("Item updated successfully")
    else:
        st.error(f"Update failed: {res.text}")


# --- Delete Item ---
st.header("🗑️ Delete Item")
delete_id = st.number_input("Enter Item ID to Delete", min_value=1, step=1)
if st.button("Delete Item"):
    res = requests.delete(f"{API_URL}{int(delete_id)}")
    if res.status_code == 204:
        st.success("Item deleted successfully")
    else:
        st.error("Delete failed")
