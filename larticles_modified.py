import streamlit as st
import pandas as pd

def sort_csv_by_article_number(file, article_numbers, shipping_name):
    # Load the CSV file with UTF-16 encoding and tab delimiter
    df = pd.read_csv(file, encoding="UTF-16", delimiter="\t")

    # Convert 'Article number' to string to preserve alphanumeric values
    df["Article number"] = df["Article number"].astype(str)

    # Process input article numbers as strings
    article_numbers = [num.strip() for num in article_numbers.split(",")]
    df_filtered = df[df["Article number"].isin(article_numbers)]

    # Filter by shipping name unless user wants totals
    if shipping_name != "+":
        df_filtered = df_filtered[df_filtered["Shipping Name"] == shipping_name]

    # Group by Article number and sum quantities
    if "Qty" in df_filtered.columns:
        df_grouped = df_filtered.groupby("Article number", as_index=False)["Qty"].sum()
    else:
        df_grouped = df_filtered.groupby("Article number", as_index=False).size().rename(columns={"size": "Qty"})

    # Optional: join back with 'Stock' if needed
    if "Stock" in df.columns:
        stock_df = df[["Article number", "Stock"]].drop_duplicates()
        df_grouped = pd.merge(df_grouped, stock_df, on="Article number", how="left")
        df_grouped = df_grouped[["Article number", "Stock", "Qty"]]
    else:
        df_grouped = df_grouped[["Article number", "Qty"]]

    # Sort by article number
    df_sorted = df_grouped.sort_values(by="Article number")

    return df_sorted

def main():
    st.title("Article Number Sorter")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    article_numbers = st.text_area("Enter article numbers (comma-separated)")
    shipping_name = st.text_input("Enter Shipping Name (or '+' for all)")

    if uploaded_file and article_numbers and shipping_name:
        sorted_df = sort_csv_by_article_number(uploaded_file, article_numbers, shipping_name)
        st.write("### Sorted Articles Table")
        st.dataframe(sorted_df)

if __name__ == "__main__":
    main()
