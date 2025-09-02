import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change this if deploying remotely

st.title("📦 Simple Item Manager")

# --- Create Item ---
st.header("Create a New Item")
name = st.text_input("Name")
description = st.text_input("Description")
price = st.number_input("Price", min_value=0)
tax = st.number_input("Tax", min_value=0)

if st.button("Create Item"):
    item_data = {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax
    }
    response = requests.post(f"{API_URL}/items/", json=item_data)
    if response.status_code == 201:
        st.success(f"Item created: {response.json()}")
    else:
        st.error(f"Error: {response.text}")

# --- View All Items ---
st.header("View All Items")
if st.button("Load Items"):
    response = requests.get(f"{API_URL}/items/")
    if response.status_code == 200:
        items = response.json()
        for item in items:
            st.write(item)
    else:
        st.error("Failed to load items")

# --- Delete Item ---
st.header("Delete an Item")
delete_id = st.number_input("Enter Item ID to Delete", min_value=1, step=1)
if st.button("Delete Item"):
    response = requests.delete(f"{API_URL}/items/{int(delete_id)}")
    if response.status_code == 204:
        st.success("Item deleted successfully")
    else:
        st.error("Item not found")
