from flask import Blueprint, request, jsonify
from services.otp_service import generate_otp, verify_otp

otp_bp = Blueprint("otp", __name__)

@otp_bp.route("/generate-otp", methods=["POST"])
def generate():
    data = request.json
    user_id = data.get("user_id")

    otp = generate_otp(user_id)

    return jsonify({"otp": otp})

@otp_bp.route("/verify-otp", methods=["POST"])
def verify():
    data = request.json
    user_id = data.get("user_id")
    entered_otp = data.get("otp")

    if verify_otp(user_id, entered_otp):
        return jsonify({"message": "OTP verified"})
    
    return jsonify({"message": "Invalid or expired OTP"}), 400


@otp_bp.route("/hospital/send-otp", methods=["POST"])
def hospital_send_otp():
    data = request.json
    patient_id = data.get("patient_id")

    otp = generate_otp(patient_id)

    return jsonify({"message": "OTP sent to patient", "patient_id": patient_id})


@otp_bp.route("/hospital/verify-otp", methods=["POST"])
def hospital_verify_otp():
    data = request.json
    patient_id = data.get("patient_id")
    otp = data.get("otp")

    if verify_otp(patient_id, otp):
        return jsonify({"message": "Patient OTP verified"})
    
    return jsonify({"message": "Invalid or expired OTP"}), 400