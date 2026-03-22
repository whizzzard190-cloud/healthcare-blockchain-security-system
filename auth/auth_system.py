import sqlite3
from utils.hash_utils import generate_hash

DB="database/healthcare.db"

# ---------------- HELPER: SAFE COLUMN ADD ----------------
def safe_add_column(cur, table, column):
    try:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")
    except:
        pass


# ---------------- PATIENT REGISTER ----------------
def patient_register(pid,password,name,age,gender,phone,
                     father=None,blood=None,dob=None,email=None):

    con=sqlite3.connect(DB)
    cur=con.cursor()

    # 🔍 Check existing
    cur.execute("SELECT * FROM patients WHERE patient_id=?", (pid,))
    existing=cur.fetchone()

    if existing:
        con.close()
        return "exists"

    # 🔥 Ensure columns exist (SAFE)
    safe_add_column(cur,"patients","father")
    safe_add_column(cur,"patients","blood")
    safe_add_column(cur,"patients","dob")
    safe_add_column(cur,"patients","email")

    # ✅ Insert full data
    cur.execute("""
    INSERT INTO patients(
        patient_id,password,name,age,gender,phone,
        father,blood,dob,email
    )
    VALUES(?,?,?,?,?,?,?,?,?,?)
    """,(pid,generate_hash(password),name,age,gender,phone,
         father,blood,dob,email))

    con.commit()
    con.close()

    return "success"


# ---------------- PATIENT LOGIN ----------------
def patient_login(pid,password):

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("""
    SELECT * FROM patients
    WHERE patient_id=? AND password=?
    """,(pid,generate_hash(password)))

    r=cur.fetchone()

    con.close()

    return r


# ---------------- HOSPITAL REGISTER ----------------
def hospital_register(hid,password,name,
                      location=None,email=None,speciality=None):

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("SELECT * FROM hospitals WHERE hospital_id=?", (hid,))
    existing=cur.fetchone()

    if existing:
        con.close()
        return "exists"

    # 🔥 Ensure columns exist
    safe_add_column(cur,"hospitals","location")
    safe_add_column(cur,"hospitals","email")
    safe_add_column(cur,"hospitals","speciality")

    # ✅ Insert full data
    cur.execute("""
    INSERT INTO hospitals(
        hospital_id,password,name,location,email,speciality
    )
    VALUES(?,?,?,?,?,?)
    """,(hid,generate_hash(password),name,location,email,speciality))

    con.commit()
    con.close()

    return "success"


# ---------------- HOSPITAL LOGIN ----------------
def hospital_login(hid,password):

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("""
    SELECT * FROM hospitals
    WHERE hospital_id=? AND password=?
    """,(hid,generate_hash(password)))

    r=cur.fetchone()

    con.close()

    return r