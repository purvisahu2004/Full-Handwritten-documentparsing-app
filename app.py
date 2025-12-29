import streamlit as st
import pandas as pd
from io import BytesIO
from handwritten_pipeline import (
    extract_employee_form_json,
    normalize_employee_json
)

st.set_page_config(page_title="Handwritten Form Extraction", layout="wide")

st.title("📝 Handwritten Form Extraction System")
st.write("handwritten document parsing")

# 🔹 Session state to store rows across reruns
if "table_data" not in st.session_state:
    st.session_state.table_data = []

uploaded_files = st.file_uploader(
    "Upload Handwritten PDF Forms (Demo Mode)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and st.button("🚀 Process Forms"):
    for file in uploaded_files:
        raw = extract_employee_form_json(file.name)
        normalized = normalize_employee_json(raw)
        st.session_state.table_data.append(normalized)

    st.success("✅ Forms processed successfully!")

# 🔹 Display table if data exists
if st.session_state.table_data:
    df = pd.DataFrame(st.session_state.table_data)

    st.subheader("📊 Extracted Employee Data")
    st.dataframe(df, use_container_width=True)

    # 🔹 Create Excel IN MEMORY
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    st.download_button(
        label="⬇ Download Excel File",
        data=excel_buffer,
        file_name="employee_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
