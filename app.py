import streamlit as st
import json
from handwritten_pipeline import (
    extract_employee_form_json,
    normalize_employee_json
)

PDF_PATH = "Employee_Information_Form.pdf"

st.set_page_config(page_title="Handwritten Form Extraction", layout="centered")

st.title("📝 Handwritten Employee Form Extraction")
st.write("AI-based document parsing using Gemini Vision")

st.info(f"Using file: `{PDF_PATH}`")

if st.button("🚀 Extract & Convert to Digital Data"):
    with st.spinner("Processing handwritten form..."):
        raw_data = extract_employee_form_json(PDF_PATH)
        final_data = normalize_employee_json(raw_data)

    if not final_data:
        st.error("Extraction failed.")
    else:
        st.success("Extraction completed successfully!")

        st.subheader("📦 Final Industrial-Level JSON")
        st.json(final_data)

        st.download_button(
            label="⬇ Download JSON",
            data=json.dumps(final_data, indent=4),
            file_name="employee_data.json",
            mime="application/json"
        )
