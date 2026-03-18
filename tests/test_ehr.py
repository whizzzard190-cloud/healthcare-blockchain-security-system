import requests

BASE_URL = "http://127.0.0.1:5000"

def test_ehr_creation():
    data = {
        "patient_id": "1",
        "doctor_id": "101",
        "diagnosis": "Flu",
        "treatment": "Rest",
        "prescription": "Paracetamol"
    }

    response = requests.post(f"{BASE_URL}/ehr/create", json=data)
    print(response.json())

if __name__ == "__main__":
    test_ehr_creation()