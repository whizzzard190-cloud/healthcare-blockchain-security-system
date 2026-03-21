import streamlit as st
import sqlite3
import time
from auth.auth_system import patient_login, patient_register, hospital_login, hospital_register
from streamlit_autorefresh import st_autorefresh

DB="database/healthcare.db"

st.set_page_config(page_title="Blockchain Healthcare",layout="centered")

# ---------------- AUTO LOGOUT ----------------
SESSION_LIMIT = 1800

if "login_time" not in st.session_state:
    st.session_state.login_time = None

if st.session_state.login_time:
    elapsed = time.time() - st.session_state.login_time

    if elapsed > SESSION_LIMIT:
        st.session_state.clear()
        st.warning("Session expired. Please login again.")
        st.stop()

    remaining = int(SESSION_LIMIT - elapsed)
else:
    remaining = SESSION_LIMIT

st_autorefresh(interval=1000, key="timer_refresh")

# ---------------- UI ----------------
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "main"

# ---------------- MAIN ----------------
if st.session_state.page == "main":

    st.markdown("<h1 style='text-align:center;color:#4CAF50'>🏥 Blockchain Healthcare</h1>",unsafe_allow_html=True)
    st.divider()

    menu=st.sidebar.selectbox(
        "Select Role",
        ["Patient Login","Patient Signup","Hospital Login","Hospital Signup"],
    )

    if menu=="Patient Signup":

        pid=st.text_input("Patient ID")
        password=st.text_input("Password",type="password")
        name=st.text_input("Full Name")
        age=st.number_input("Age",min_value=1)
        gender=st.selectbox("Gender",["M","F"])
        phone=st.text_input("Phone")

        if st.button("Register"):
            result = patient_register(pid,password,name,age,gender,phone)

            if result=="exists":
                st.error("Patient ID already exists")
            else:
                st.success("Patient Registered Successfully")

    if menu=="Hospital Signup":

        hid=st.text_input("Hospital ID")
        name=st.text_input("Hospital Name")
        password=st.text_input("Password",type="password")

        if st.button("Register Hospital"):
            result = hospital_register(hid,password,name)

            if result=="exists":
                st.error("Hospital already exists")
            else:
                st.success("Hospital Registered Successfully")

    if menu=="Patient Login":

        pid=st.text_input("Patient ID")
        password=st.text_input("Password",type="password")

        if st.button("Login"):
            user=patient_login(pid,password)

            if user:
                st.session_state.pid = pid
                st.session_state.page = "patient_dashboard"
                st.session_state.login_time = time.time()
                st.rerun()
            else:
                st.error("Invalid Credentials")

    if menu=="Hospital Login":

        hid=st.text_input("Hospital ID")
        password=st.text_input("Password",type="password")

        if st.button("Login"):
            hosp=hospital_login(hid,password)

            if hosp:
                st.session_state.hid=hid
                st.session_state.page="hospital_dashboard"
                st.session_state.login_time = time.time()
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------------- PATIENT DASHBOARD ----------------
elif st.session_state.page == "patient_dashboard":

    st.markdown("## 🧑 Patient Dashboard")
    st.caption(f"⏳ Auto logout in {remaining//60} min {remaining%60} sec")

    if st.button("📜 Medical History"):
        st.session_state.page = "patient_history"
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ---------------- PATIENT HISTORY ----------------
elif st.session_state.page == "patient_history":

    st.markdown("## 📜 Medical History")
    st.caption(f"⏳ Auto logout in {remaining//60} min {remaining%60} sec")

    if st.button("⬅ Back"):
        st.session_state.page = "patient_dashboard"
        st.rerun()

    pid = st.session_state.get("pid")

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("""
    SELECT h.name,h.location,a.date,t.amount,a.notes
    FROM appointments a
    JOIN hospitals h ON a.hospital_id=h.hospital_id
    JOIN transactions t ON a.id=t.appointment_id
    WHERE a.patient_id=?
    ORDER BY a.date DESC
    """,(pid,))

    data=cur.fetchall()
    con.close()

    for row in data:
        with st.container(border=True):
            st.markdown(f"**🏥 {row[0]}**")
            st.write(f"📍 {row[1]}")
            st.write(f"📅 {row[2]}")
            st.write(f"💰 ₹{row[3]}")
            st.write(f"📝 {row[4]}")

# ---------------- HOSPITAL DASHBOARD ----------------
elif st.session_state.page == "hospital_dashboard":

    st.markdown("## 🏥 Hospital Dashboard")
    st.caption(f"⏳ Auto logout in {remaining//60} min {remaining%60} sec")

    if st.button("📝 Update"):
        st.session_state.page = "update_record"
        st.rerun()

    if st.button("📜 History"):
        st.session_state.page = "view_patient_history"
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ---------------- UPDATE RECORD ----------------
elif st.session_state.page == "update_record":

    st.markdown("## 📝 Update Record")
    st.caption(f"⏳ Auto logout in {remaining//60} min {remaining%60} sec")

    if st.button("⬅ Back"):
        st.session_state.page = "hospital_dashboard"
        st.rerun()

    hid = st.session_state.get("hid")

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("SELECT patient_id FROM patients")
    patients=[p[0] for p in cur.fetchall()]

    selected=st.selectbox("Select Patient",patients)

    category=st.selectbox("Medical Category",
        ["Routine","BP","MRI","Surgery","Diabetes","Chest Pain","Physio","Neuro","Cardiac","Ortho"]
    )

    note=st.text_area("Doctor Notes")

    if st.button("Submit"):

        final_note=f"{category}: {note}"

        cur.execute("""
        INSERT INTO appointments(patient_id,hospital_id,date,notes)
        VALUES(?,?,DATE('now'),?)
        """,(selected,hid,final_note))

        appointment_id=cur.lastrowid

        cur.execute("""
        INSERT INTO transactions(appointment_id,amount,status)
        VALUES(?,?,?)
        """,(appointment_id,500,"PAID"))

        con.commit()
        con.close()

        st.success("Record Updated")

# ---------------- VIEW PATIENT HISTORY ----------------
elif st.session_state.page == "view_patient_history":

    st.markdown("## 📜 Patient History")
    st.caption(f"⏳ Auto logout in {remaining//60} min {remaining%60} sec")

    if st.button("⬅ Back"):
        st.session_state.page = "hospital_dashboard"
        st.rerun()

    if "history_pid" not in st.session_state:
        st.session_state.history_pid = ""

    if "history_data" not in st.session_state:
        st.session_state.history_data = []

    pid = st.text_input("Enter Patient ID", value=st.session_state.history_pid)
    st.session_state.history_pid = pid

    if st.button("Load"):

        con=sqlite3.connect(DB)
        cur=con.cursor()

        cur.execute("""
        SELECT h.name,h.location,a.date,t.amount,a.notes
        FROM appointments a
        JOIN hospitals h ON a.hospital_id=h.hospital_id
        JOIN transactions t ON a.id=t.appointment_id
        WHERE a.patient_id=?
        ORDER BY a.date DESC
        """,(pid,))

        st.session_state.history_data = cur.fetchall()
        con.close()

    for row in st.session_state.history_data:
        with st.container(border=True):
            st.markdown(f"**🏥 {row[0]}**")
            st.write(f"📍 {row[1]}")
            st.write(f"📅 {row[2]}")
            st.write(f"💰 ₹{row[3]}")
            st.write(f"📝 {row[4]}")