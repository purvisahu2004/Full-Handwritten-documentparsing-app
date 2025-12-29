import re
from datetime import datetime

# DEMO MODE
DEMO_MODE = True


def extract_employee_form_json(file_name: str) -> dict:
    if DEMO_MODE:
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

    raise RuntimeError("Real mode disabled")


def normalize_employee_json(data: dict) -> dict:
    def clean_phone(p):
        return re.sub(r"\D", "", p) if p else ""

    def normalize_date(d):
        try:
            return datetime.strptime(d, "%m/%d/%Y").date().isoformat()
        except:
            return d

    return {
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
