import time
import uuid

session_store = {}

SESSION_DURATION = 1800

def create_session(user_id):
    session_id = str(uuid.uuid4())
    expiry = time.time() + SESSION_DURATION

    session_store[session_id] = {
        "user_id": user_id,
        "expiry": expiry
    }

    return session_id


def validate_session(session_id):
    if session_id not in session_store:
        return None

    session = session_store[session_id]

    if time.time() > session["expiry"]:
        del session_store[session_id]
        return None

    return session["user_id"]


def destroy_session(session_id):
    if session_id in session_store:
        del session_store[session_id]