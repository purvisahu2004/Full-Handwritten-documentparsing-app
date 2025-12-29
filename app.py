import streamlit as st
import pandas as pd
from handwritten_pipeline import (
    extract_employee_form_json,
    normalize_employee_json,
    append_to_excel
)

st.set_page_config(page_title="Handwritten Form Extraction", layout="wide")

st.title("📝 Handwritten Form Extraction System")
st.write("Upload multiple handwritten employee forms and convert them to digital data.")

uploaded_files = st.file_uploader(
    "Upload Handwritten Form PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    all_rows = []

    if st.button("🚀 Process Forms"):
        with st.spinner("Processing forms..."):
            for file in uploaded_files:
                with open(file.name, "wb") as f:
                    f.write(file.getbuffer())

                raw = extract_employee_form_json(file.name)
                normalized = normalize_employee_json(raw)
                all_rows.append(normalized)

                append_to_excel(normalized)

        st.success("✅ All forms processed and saved to Excel!")

        df = pd.DataFrame(all_rows)

        st.subheader("📊 Extracted Data (Tabular View)")
        st.dataframe(df)

        with open("output.xlsx", "rb") as f:
            st.download_button(
                "⬇ Download Excel File",
                f,
                file_name="employee_data.xlsx"
            )
