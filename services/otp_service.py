import random
import time

otp_store = {}

def generate_otp(user_id):
    otp = str(random.randint(100000, 999999))
    expiry = time.time() + 300
    otp_store[user_id] = {"otp": otp, "expiry": expiry}
    return otp

def verify_otp(user_id, entered_otp):
    if user_id not in otp_store:
        return False

    record = otp_store[user_id]

    if time.time() > record["expiry"]:
        del otp_store[user_id]
        return False

    if record["otp"] == entered_otp:
        del otp_store[user_id]
        return True

    return False