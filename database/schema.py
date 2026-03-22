import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
import random
from utils.hash_utils import generate_hash

NOTES=[
"Routine Checkup",
"Blood Pressure Review",
"MRI Review",
"Post Surgery Consultation",
"Diabetes Monitoring",
"Chest Pain Evaluation",
"Physiotherapy Session",
"Neurology Assessment",
"Cardiac Stress Test",
"Orthopedic Review"
]

DB="database/healthcare.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------- HOSPITAL TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS hospitals(
hospital_id TEXT PRIMARY KEY,
password TEXT,
name TEXT,
location TEXT,
speciality TEXT
)
""")

# ---------------- PATIENT TABLE (UPDATED) ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS patients(
patient_id TEXT PRIMARY KEY,
password TEXT,
name TEXT,
age INTEGER,
gender TEXT,
phone TEXT,
father TEXT,
blood TEXT,
dob TEXT,
email TEXT
)
""")

# ---------------- SAFE ADD FOR OLD DB ----------------
def safe_add_patient_column(column):
    try:
        cur.execute(f"ALTER TABLE patients ADD COLUMN {column} TEXT")
    except:
        pass

safe_add_patient_column("father")
safe_add_patient_column("blood")
safe_add_patient_column("dob")
safe_add_patient_column("email")

# ---------------- APPOINTMENTS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS appointments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
patient_id TEXT,
hospital_id TEXT,
date TEXT,
notes TEXT,
prescription TEXT,
diagnosis TEXT,
symptoms TEXT,
tests TEXT,
advice TEXT
)
""")

# ---------------- SAFE ADD (APPOINTMENTS) ----------------
def safe_add_column(column):
    try:
        cur.execute(f"ALTER TABLE appointments ADD COLUMN {column} TEXT")
    except:
        pass

safe_add_column("prescription")
safe_add_column("diagnosis")
safe_add_column("symptoms")
safe_add_column("tests")
safe_add_column("advice")

# ---------------- TRANSACTIONS ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
appointment_id INTEGER,
amount INTEGER,
status TEXT
)
""")

# ---------------- BLOCKCHAIN ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS blockchain_ledger(
id INTEGER PRIMARY KEY AUTOINCREMENT,
data TEXT,
hash TEXT,
previous_hash TEXT
)
""")

# ---------------- INSERT HOSPITALS ----------------
hospitals = [
("H001",generate_hash("admin123"),"Apollo Hospitals","Hyderabad","Cardiology"),
("H002",generate_hash("admin123"),"Yashoda Hospitals","Hyderabad","Neurology"),
("H003",generate_hash("admin123"),"KIMS","Hyderabad","Orthopedics"),
("H004",generate_hash("admin123"),"Care Hospitals","Hyderabad","Oncology"),
("H005",generate_hash("admin123"),"AIG Hospitals","Hyderabad","Gastroenterology"),
("H006",generate_hash("admin123"),"Rainbow Hospitals","Hyderabad","Pediatrics"),
("H007",generate_hash("admin123"),"Continental Hospitals","Hyderabad","Nephrology"),
("H008",generate_hash("admin123"),"Sunshine Hospitals","Hyderabad","Traumatology"),
("H009",generate_hash("admin123"),"Star Hospitals","Hyderabad","Pulmonology"),
("H010",generate_hash("admin123"),"Omega Hospitals","Hyderabad","Radiology")
]

cur.executemany("INSERT OR IGNORE INTO hospitals VALUES (?,?,?,?,?)", hospitals)

conn.commit()
conn.close()

print("Database & tables created successfully")

# ---------------- ADD APPOINTMENT ----------------
def add_appointment(pid,hid,date,amount):
    from blockchain.ledger import Blockchain

    note=random.choice(NOTES)

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("""
    INSERT INTO appointments(
        patient_id,hospital_id,date,notes,
        prescription,diagnosis,symptoms,tests,advice
    )
    VALUES(?,?,?,?,?,?,?,?,?)
    """,(pid,hid,date,note,
         "Paracetamol",
         "General Checkup",
         "Fever",
         "Blood Test",
         "Rest and hydration"))

    appointment_id=cur.lastrowid

    cur.execute("""
    INSERT INTO transactions(appointment_id,amount,status)
    VALUES(?,?,?)
    """,(appointment_id,amount,"PAID"))

    con.commit()
    con.close()

    bc=Blockchain()
    bc.add_block(f"{pid}-{hid}-{date}-{amount}")

# ---------------- SEED DATA ----------------
def seed_data():
    from auth.auth_system import patient_register

    hospitals=["H001","H002","H003","H004","H005","H006","H007","H008","H009","H010"]

    for i in range(1,21):

        pid=f"P{i:03}"

        # ✅ UPDATED REGISTER CALL
        patient_register(
            pid,"pass123",
            f"Patient{i}",
            random.randint(20,60),
            "M",
            "9000000000",
            "FatherName",
            "O+",
            "01-01-2000",
            "test@mail.com"
        )

        visited=random.sample(hospitals, random.randint(5,10))

        for hid in visited:
            date=f"2026-02-{random.randint(1,28)}"
            amount=random.randint(300,2000)
            add_appointment(pid,hid,date,amount)

    print("20 patients with full medical history inserted")