import re
import pandas as pd
from datetime import datetime

# ==========================================================
# 🔴 DEMO MODE FLAG
# ==========================================================
# True  → Cloud / Presentation / Demo (NO API CALLS)
# False → Local machine with Gemini API
DEMO_MODE = True


# ==========================================================
# HANDWRITTEN EXTRACTION (DEMO / REAL SWITCH)
# ==========================================================
def extract_employee_form_json(file_path: str) -> dict:
    """
    In DEMO_MODE:
        Returns mock extracted data (simulates Gemini OCR output)
    In REAL mode:
        Gemini OCR logic can be added later
    """

    if DEMO_MODE:
        # 🔹 MOCK DATA (REALISTIC HANDWRITTEN OUTPUT)
        return {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "03/15/1985",
            "email": "john.doe@email.com",
            "phone_number": "(217) 555-7890",
            "position": "Sales Associate",
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "(217) 555-1234"
        }

    # ------------------------------------------------------
    # REAL GEMINI LOGIC (USE ONLY LOCALLY)
    # ------------------------------------------------------
    raise RuntimeError(
        "REAL MODE disabled in demo. Set DEMO_MODE=False to enable Gemini."
    )


# ==========================================================
# NORMALIZATION (INDUSTRIAL LEVEL)
# ==========================================================
def normalize_employee_json(data: dict) -> dict:

    def clean_phone(phone):
        return re.sub(r"\D", "", phone) if phone else ""

    def normalize_date(d):
        try:
            return datetime.strptime(d, "%m/%d/%Y").date().isoformat()
        except:
            return d

    normalized = {
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "date_of_birth": normalize_date(data.get("date_of_birth", "")),
        "email": data.get("email", "").lower(),
        "phone_number": clean_phone(data.get("phone_number", "")),
        "position": data.get("position", "").lower().replace(" ", "_"),
        "emergency_contact_name": data.get("emergency_contact_name", ""),
        "emergency_contact_phone": clean_phone(
            data.get("emergency_contact_phone", "")
        )
    }

    return normalized


# ==========================================================
# APPEND MULTIPLE ROWS TO EXCEL
# ==========================================================
def append_to_excel(data: dict, filename="employee_output.xlsx"):
    df_new = pd.DataFrame([data])

    try:
        df_existing = pd.read_excel(filename)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    except FileNotFoundError:
        df_final = df_new

    df_final.to_excel(filename, index=False)
    return df_final

