import pandas as pd
import streamlit as st

# Streamlit title and file uploader
st.title("Orderanalys på kundnivå")

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    # Read the file
    try:
        data = pd.read_csv(uploaded_file, encoding='utf-16', sep='\t')
    except Exception as e:
        st.error(f"Failed to read the file: {e}")
        st.stop()

    # Function to handle order times
    def order_time():
        data['Order time'] = pd.to_datetime(
            data['Order time'], errors='coerce')

        # Find first and last order time
        first_order_time = data['Order time'].min()
        last_order_time = data['Order time'].max()

        st.write(f"**First Order Time:** {first_order_time}")
        st.write(f"**Last Order Time:** {last_order_time}")

    order_time()

    # Check required columns
    required_columns = ['Order ID', 'Product',
                        'Quantity', 'Shipping Name', 'Article number']
    if all(column in data.columns for column in required_columns):
        # Group data by Order ID
        grouped_data = data.groupby('Order ID').agg({
            'Product': lambda x: ', '.join(map(str, x)),
            'Quantity': lambda x: ', '.join(map(str, x)),
            'Shipping Name': 'first',
            'Article number': lambda x: ', '.join(map(str, x))
        }).reset_index()

        # Display grouped data
        st.subheader("Grouped Data")
        st.dataframe(grouped_data)

        # Input for Shipping Name filter
        shipping_name_to_filter = st.text_input(
            "Enter Shipping Name to filter:", "Apohem AB")

        if shipping_name_to_filter:
            # Filter data by Shipping Name
            filtered_orders = grouped_data[grouped_data['Shipping Name']
                                           == shipping_name_to_filter]

            # Display filtered grouped data
            st.subheader(
                f"Filtered Grouped Data for Shipping Name: {shipping_name_to_filter}")
            st.dataframe(filtered_orders)

            # Expand products, article numbers, and quantities
            expanded_data = []
            for _, row in filtered_orders.iterrows():
                products = row['Product'].split(', ')
                article_numbers = row['Article number'].split(', ')
                quantities = row['Quantity'].split(', ')

                for product, article_number, quantity in zip(products, article_numbers, quantities):
                    expanded_data.append({
                        'Product': product.strip(),
                        'Article number': article_number.strip(),
                        'Quantity': int(quantity.strip())
                    })

            # Create a detailed table
            detailed_table = pd.DataFrame(expanded_data).groupby(['Product', 'Article number'], as_index=False).agg({
                'Quantity': 'sum'
            })

            # Display results
            st.subheader(
                f"Detailed Products for Shipping Name: {shipping_name_to_filter}")
            st.dataframe(detailed_table)

            # Download results
            output_csv = detailed_table.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="Download Filtered Data as CSV",
                data=output_csv,
                file_name="filtered_products_articles_with_quantities.csv",
                mime="text/csv"
            )
        else:
            st.warning("Please enter a valid Shipping Name to filter. Det behöver vara exakt som det står under leverans under Företag. Inga mellanslag")
    else:
        st.error("The required columns ('Order ID', 'Product', 'Quantity', 'Shipping Name', 'Article number') are not in the dataset.")
else:
    st.info("Please upload a CSV file to start.")
