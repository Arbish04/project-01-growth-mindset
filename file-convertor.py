import streamlit as st
import pandas as pd
from io import BytesIO


# Streamlit page configuration
st.set_page_config(page_title="File Convertor", layout="wide")

st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader
files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        try:
            if ext == "csv":
                df = pd.read_csv(file)
            else:
                import openpyxl  # Ensure openpyxl is available for Excel files
                df = pd.read_excel(file, engine="openpyxl")

            st.subheader(f"{file.name} - Preview")
            st.dataframe(df.head())

            # Fill missing values
            if st.checkbox(f"Fill Missing Values - ({file.name})"):
                df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                st.success("Missing Values filled with mean")
                st.dataframe(df.head())

            # Column selection
            selected_columns = st.multiselect(
                f"Select Columns - ({file.name})", df.columns, default=df.columns
            )
            df = df[selected_columns]
            st.dataframe(df.head())

            # Show chart
            if st.checkbox(f"Show Chart - ({file.name})") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            # File format choice
            format_choice = st.radio(
                f"Convert {file.name} to:", ["csv", "Excel"], key=file.name
            )

            # Download button
            if st.button(f"Download {file.name} as {format_choice}"):
                output = BytesIO()
                if format_choice == "csv":
                    df.to_csv(output, index=False)
                    mime = "text/csv"
                    new_name = file.name.replace(ext, "csv")
                else:
                    df.to_excel(output, index=False, engine="openpyxl")
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button(
                    label="Download File",
                    data=output,
                    file_name=new_name,
                    mime=mime,
                )
                st.success("Processing Complete!")

        except ImportError:
            st.error("Error: Missing dependency 'openpyxl'. Install it using 'pip install openpyxl'.")
