from flask import Blueprint, request, jsonify
from database.db_config import get_db_connection
from utils.ehr_validator import validate_ehr
from utils.encryption import encrypt_data
from blockchain.blockchain import Blockchain

ehr_bp = Blueprint("ehr", __name__)
blockchain = Blockchain()

@ehr_bp.route("/ehr/create", methods=["POST"])
def create_ehr():
    data = request.json

    if not validate_ehr(data):
        return jsonify({"message": "Invalid data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    encrypted_diagnosis = encrypt_data(data.get("diagnosis", ""))
    encrypted_treatment = encrypt_data(data.get("treatment", ""))
    encrypted_prescription = encrypt_data(data.get("prescription", ""))

    cursor.execute("""
        INSERT INTO ehr (patient_id, doctor_id, diagnosis, treatment, prescription)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["patient_id"],
        data["doctor_id"],
        encrypted_diagnosis,
        encrypted_treatment,
        encrypted_prescription
    ))

    conn.commit()

    blockchain.add_ehr_record(data)

    return jsonify({"message": "EHR created"})