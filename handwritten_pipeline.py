import json
import re
from datetime import datetime
import pandas as pd
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDr4972UCNvTnxGlLw7PNpoVkfNTvBAFoU")


# ==========================================================
# EXTRACTION
# ==========================================================
def extract_employee_form_json(pdf_path: str) -> dict:
    uploaded = genai.upload_file(pdf_path)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    response = model.generate_content([
        uploaded,
        """
        You are given a scanned handwritten Employee Information Form.

        Extract employee details such as:
        first_name, last_name, date_of_birth, phone_number, email,
        address, position, emergency contact.

        Use snake_case keys.
        Return ONLY valid JSON.
        """
    ])

    raw = (response.text or "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        return json.loads(match.group(0)) if match else {}


# ==========================================================
# NORMALIZATION
# ==========================================================
def normalize_employee_json(data: dict) -> dict:

    def clean_phone(p):
        return re.sub(r"\D", "", p) if p else ""

    def normalize_date(d):
        for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(d, fmt).date().isoformat()
            except:
                pass
        return d

    normalized = {
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "date_of_birth": normalize_date(data.get("date_of_birth", "")),
        "email": data.get("email", "").lower(),
        "phone_number": clean_phone(data.get("phone_number", "")),
        "position": data.get("position", "").lower(),
        "emergency_contact_name": data.get("emergency_contact_name", ""),
        "emergency_contact_phone": clean_phone(
            data.get("emergency_contact_phone", "")
        )
    }

    return normalized


# ==========================================================
# SAVE / APPEND TO EXCEL
# ==========================================================
def append_to_excel(data: dict, filename="output.xlsx"):
    df_new = pd.DataFrame([data])

    if os.path.exists(filename):
        df_existing = pd.read_excel(filename)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(filename, index=False)
    return df_final
