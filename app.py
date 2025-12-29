import streamlit as st
import time
import pandas as pd
from handwritten_pipeline import (
    extract_employee_form_json,
    normalize_employee_json,
    append_to_excel
)

st.set_page_config(page_title="Handwritten Form Extraction", layout="wide")

st.title("📝 Handwritten Form Extraction System")
st.write("Upload handwritten employee forms and convert them into Excel data.")

uploaded_files = st.file_uploader(
    "Upload Handwritten PDF Forms (Max 3)",
    type=["pdf"],
    accept_multiple_files=True
)

# LIMIT FILES TO AVOID QUOTA ISSUES
if uploaded_files and len(uploaded_files) > 3:
    st.warning("Please upload a maximum of 3 files at a time (API limit).")
    st.stop()

if uploaded_files:
    if st.button("🚀 Process Forms"):
        all_rows = []

        with st.spinner("Processing handwritten forms..."):
            for file in uploaded_files:
                # Save file locally
                with open(file.name, "wb") as f:
                    f.write(file.getbuffer())

                # AI extraction
                raw_data = extract_employee_form_json(file.name)

                # Normalization
                normalized = normalize_employee_json(raw_data)
                all_rows.append(normalized)

                # Append to Excel
                append_to_excel(normalized)

                # RATE LIMITING (VERY IMPORTANT)
                time.sleep(2)

        df = pd.DataFrame(all_rows)

        st.success("✅ Forms processed successfully!")

        st.subheader("📊 Extracted Data (Tabular View)")
        st.dataframe(df, use_container_width=True)

        with open("employee_output.xlsx", "rb") as f:
            st.download_button(
                "⬇ Download Excel File",
                f,
                file_name="employee_output.xlsx"
            )
