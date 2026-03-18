import sqlite3
from utils.hash_utils import generate_hash

DB="database/healthcare.db"

def patient_register(pid,password,name,age,gender,phone):

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("SELECT * FROM patients WHERE patient_id=?", (pid,))
    existing=cur.fetchone()

    if existing:
        con.close()
        return "exists"

    cur.execute("""
    INSERT INTO patients(patient_id,password,name,age,gender,phone)
    VALUES(?,?,?,?,?,?)
    """,(pid,generate_hash(password),name,age,gender,phone))

    con.commit()
    con.close()

    return "success"


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


def hospital_register(hid,password,name):

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("SELECT * FROM hospitals WHERE hospital_id=?", (hid,))
    existing=cur.fetchone()

    if existing:
        con.close()
        return "exists"

    cur.execute("""
    INSERT INTO hospitals(hospital_id,password,name)
    VALUES(?,?,?)
    """,(hid,generate_hash(password),name))

    con.commit()
    con.close()

    return "success"


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