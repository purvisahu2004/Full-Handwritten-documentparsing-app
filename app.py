import streamlit as st
import pandas as pd
from handwritten_pipeline import (
    extract_employee_form_json,
    normalize_employee_json,
    append_to_excel
)

st.set_page_config(
    page_title="Handwritten Form Extraction",
    layout="wide"
)

st.title("📝 Handwritten Form Extraction System")
st.write(
    "This application converts handwritten employee forms into "
    "structured digital data and Excel format."
)

uploaded_files = st.file_uploader(
    "Upload Handwritten PDF Forms (Demo Mode)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 Process Forms"):
        all_rows = []

        with st.spinner("Processing handwritten forms..."):
            for file in uploaded_files:
                # 🔹 DEMO: no need to save file
                raw_data = extract_employee_form_json(file.name)
                normalized = normalize_employee_json(raw_data)
                all_rows.append(normalized)
                append_to_excel(normalized)

        df = pd.DataFrame(all_rows)

        st.success("✅ Forms processed successfully!")

        st.subheader("📊 Extracted Employee Data")
        st.dataframe(df, use_container_width=True)

        with open("employee_output.xlsx", "rb") as f:
            st.download_button(
                label="⬇ Download Excel File",
                data=f,
                file_name="employee_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
