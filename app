import streamlit as st
import pandas as pd

def process_shipping_name(data, shipping_name):
    # Check if 'Shipping name' exists
    if 'Shipping name' not in data.columns:
        st.error("Fil har ej kolumn shipping name exporters file med leveransadress")
        return None

    # Filter for the specific shipping name
    filtered_data = data[data['Shipping name'] == shipping_name]

    if filtered_data.empty:
        st.warning(f"No data found for Shipping name: {shipping_name}")
        return None

    # Extract distinct products
    distinct_products = filtered_data['Product'].drop_duplicates()
    return distinct_products

# Streamlit app layout
st.title("Shipping Name Filter App")
st.write("Upload a file and filter data by a specific shipping name.")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load the file
        data = pd.read_csv(uploaded_file, encoding='utf-16', sep='\t')
        st.success("File uploaded and loaded successfully!")

        # Display a sample of the data
        if st.checkbox("Show raw data"):
            st.write(data)

        # Input for shipping name
        shipping_name = st.text_input("Enter the specific Shipping Name", "Bubbel & Plask Simskolor AB")

        if shipping_name:
            # Process the data
            result = process_shipping_name(data, shipping_name)

            if result is not None:
                st.write(f"Distinct products for Shipping name: **{shipping_name}**")
                st.table(result)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
