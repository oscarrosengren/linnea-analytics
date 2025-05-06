
import streamlit as st
import pandas as pd

def sort_csv_by_article_number(file, article_numbers, shipping_name):
    # Load the CSV file with UTF-16 encoding and tab delimiter
    df = pd.read_csv(file, encoding="UTF-16", delimiter="\t")

    # Convert 'Article number' and 'Shipping Name' to string to preserve alphanumeric values
    df["Article number"] = df["Article number"].astype(str)
    if "Shipping Name" in df.columns:
        df["Shipping Name"] = df["Shipping Name"].astype(str)

    # Process input article numbers as strings
    article_numbers = [num.strip() for num in article_numbers.split(",")]
    df_filtered = df[df["Article number"].isin(article_numbers)]

    # If "Shipping Name" exists and a filter is specified
    if "Shipping Name" in df.columns and shipping_name:
        if shipping_name.strip() == "+":
            # Group by 'Shipping Name' and sum numeric columns
            df_filtered = df_filtered.groupby("Shipping Name", as_index=False).sum(numeric_only=True)
        else:
            df_filtered = df_filtered[df_filtered["Shipping Name"] == shipping_name.strip()]

    # Sort the dataframe by 'Article number' if it's still present
    if "Article number" in df_filtered.columns:
        df_filtered = df_filtered.sort_values(by="Article number")

    # Reorder columns to place 'Stock' after 'Article number'
    if "Stock" in df_filtered.columns and "Article number" in df_filtered.columns:
        columns = ["Article number", "Stock"] + [col for col in df_filtered.columns if col not in ["Article number", "Stock"]]
        df_filtered = df_filtered[columns]

    return df_filtered

def main():
    st.title("Article Number Sorter with Shipping Name Filter")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    article_numbers = st.text_area("Enter article numbers (comma-separated)")
    shipping_name = st.text_input("Enter Shipping Name (or '+' for all)")

    if uploaded_file and article_numbers:
        sorted_df = sort_csv_by_article_number(uploaded_file, article_numbers, shipping_name)
        st.write("### Filtered and Sorted Articles Table")
        st.dataframe(sorted_df)

if __name__ == "__main__":
    main()
