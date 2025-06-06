import streamlit as st
import pandas as pd

# Load the Excel file once when the app starts
@st.cache_data
def load_data(filepath):
    return pd.read_excel(filepath)

# Path to your Excel file (change this if needed)
EXCEL_FILE_PATH = "erp_outlook_joined_final.xlsx"
df = load_data(EXCEL_FILE_PATH)

# Define valid columns for searching
valid_columns = ["Class", "Manufacturer Part Number", "Manufacturer Number", "Manufacturer"]

# UI Title
st.title("🔍 Excel Data Search Tool")

# Field Selection
selected_column = st.selectbox("Choose the field to search in:", valid_columns)

# Input text to search
search_text = st.text_input(f"Enter the substring to search in '{selected_column}':")

# Search Function
def search_rows(column_name, search_value):
    mask = df[column_name].astype(str).str.contains(str(search_value), case=False, na=False)
    return df.loc[mask].copy()

# Pretty Print Function (streamlit version)
def pretty_display_rows(rows, max_rows=10):
    if rows.empty:
        st.warning("⚠️ No matches found.")
        return
    to_show = rows.head(max_rows)
    for _, row in to_show.iterrows():
        with st.expander(f"Row Details (Index: {row.name})"):
            for col in to_show.columns:
                val = "" if pd.isna(row[col]) else row[col]
                st.markdown(f"**{col}:** {val}")
            st.markdown("---")

# Search Trigger
if search_text:
    results = search_rows(selected_column, search_text)
    st.write(f"Found {len(results)} matching row(s). Showing up to 10:")
    pretty_display_rows(results, max_rows=10)
