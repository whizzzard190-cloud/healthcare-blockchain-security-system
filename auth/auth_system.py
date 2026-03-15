import sqlite3
from utils.hash_utils import generate_hash

DB="database/healthcare.db"

def patient_register(pid,password,name,age,gender,phone):
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("INSERT INTO patients VALUES (?,?,?,?,?,?)",
    (pid,generate_hash(password),name,age,gender,phone))
    con.commit()
    con.close()

def patient_login(pid,password):
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("SELECT * FROM patients WHERE patient_id=? AND password=?",
    (pid,generate_hash(password)))
    r=cur.fetchone()
    con.close()
    return r

def hospital_login(hid,password):
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("SELECT * FROM hospitals WHERE hospital_id=? AND password=?",
    (hid,generate_hash(password)))
    r=cur.fetchone()
    con.close()
    return r
