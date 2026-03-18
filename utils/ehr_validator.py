def validate_ehr(data):
    required_fields = ["patient_id", "doctor_id"]

    for field in required_fields:
        if field not in data or not data[field]:
            return False

    return True