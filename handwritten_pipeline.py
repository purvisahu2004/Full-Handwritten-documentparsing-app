import json
import re
from datetime import datetime
import google.generativeai as genai


# ==========================================================
# GEMINI CONFIG
# ==========================================================
genai.configure(api_key="AIzaSyBmF2snZNrrRnkJpwdLOI0kRhNoM6kebXg")


# ==========================================================
# HANDWRITTEN OCR + AUTO JSON EXTRACTION
# ==========================================================
def extract_employee_form_json(pdf_path: str) -> dict:
    uploaded = genai.upload_file(pdf_path)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    response = model.generate_content([
        uploaded,
        """
        You are given a scanned handwritten Employee Information Form.

        TASK:
        - Read printed labels and handwritten values.
        - Infer snake_case field names.
        - Group related fields logically.
        - Return ONLY valid JSON.
        - No explanations, no markdown.

        Expected structure:
        {
          "employee": {...},
          "contact": {...},
          "job_details": {...},
          "emergency_contact": {...}
        }
        """
    ])

    raw = (response.text or "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        return json.loads(match.group(0)) if match else {}


# ==========================================================
# NORMALIZATION (INDUSTRIAL LEVEL)
# ==========================================================
def normalize_employee_json(data: dict) -> dict:
    def normalize_date(d):
        try:
            return datetime.strptime(d, "%m/%d/%Y").date().isoformat()
        except:
            return d

    def clean_phone(p):
        return re.sub(r"\D", "", p)

    normalized = {}

    # Employee
    emp = data.get("employee", {})
    normalized["employee"] = {
        "first_name": emp.get("first_name", "").strip(),
        "last_name": emp.get("last_name", "").strip(),
        "date_of_birth": normalize_date(emp.get("date_of_birth", "")),
        "ssn": emp.get("ssn", ""),
        "start_date": normalize_date(emp.get("start_date", "")),
        "signature_name": emp.get("signature_name", "")
    }

    # Contact
    con = data.get("contact", {})
    normalized["contact"] = {
        "email": con.get("email", "").lower(),
        "phone_number": clean_phone(con.get("phone_number", "")),
        "address": con.get("address", {})
    }

    # Job
    job = data.get("job_details", {})
    normalized["job_details"] = {
        "position": job.get("position", "").lower().replace(" ", "_")
    }

    # Emergency Contact
    ec = data.get("emergency_contact", {})
    normalized["emergency_contact"] = {
        "name": ec.get("name", ""),
        "relationship": ec.get("relationship", "").lower(),
        "phone": clean_phone(ec.get("phone", ""))
    }

    return normalized
