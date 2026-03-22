import streamlit as st
import sqlite3
import time
from auth.auth_system import patient_login, patient_register, hospital_login, hospital_register
from streamlit_autorefresh import st_autorefresh

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

DB="database/healthcare.db"

st.set_page_config(page_title="Blockchain Healthcare",layout="wide")

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

# 🔥 FIX: slower refresh
st_autorefresh(interval=5000, key="timer_refresh")

# ---------------- MESSAGE SYSTEM ----------------
if "msg" not in st.session_state:
    st.session_state.msg = None

if "msg_time" not in st.session_state:
    st.session_state.msg_time = 0

if st.session_state.msg:
    if time.time() - st.session_state.msg_time < 3:
        if st.session_state.msg[0] == "success":
            st.success(st.session_state.msg[1])
        else:
            st.error(st.session_state.msg[1])
    else:
        st.session_state.msg = None

# ---------------- UI STYLE ----------------
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

# ---------------- PDF ----------------
def generate_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Medical Report", styles['Title']))
    elements.append(Spacer(1, 12))

    for row in data:
        elements.append(Paragraph(f"Hospital: {row[0]}", styles['Normal']))
        elements.append(Paragraph(f"Location: {row[1]}", styles['Normal']))
        elements.append(Paragraph(f"Date: {row[2]}", styles['Normal']))
        elements.append(Paragraph(f"Amount: ₹{row[3]}", styles['Normal']))
        elements.append(Paragraph(f"Notes: {row[4]}", styles['Normal']))
        elements.append(Paragraph(f"Prescription: {row[5]}", styles['Normal']))
        elements.append(Paragraph(f"Diagnosis: {row[6]}", styles['Normal']))
        elements.append(Paragraph(f"Symptoms: {row[7]}", styles['Normal']))
        elements.append(Paragraph(f"Tests: {row[8]}", styles['Normal']))
        elements.append(Paragraph(f"Advice: {row[9]}", styles['Normal']))
        elements.append(Spacer(1, 20))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- MAIN ----------------
if st.session_state.page == "main":

    st.markdown("<h1 style='text-align:center;'>Blockchain-Based Health Record Management</h1>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏥 Hospital Login")

        hid = st.text_input("Hospital Username", key="hosp_user")
        hpass = st.text_input("Hospital Password", type="password", key="hosp_pass")

        if st.button("LOGIN", key="hosp_login"):
            if hospital_login(hid, hpass):
                st.session_state.hid = hid
                st.session_state.page = "hospital_dashboard"
                st.session_state.login_time = time.time()
                st.rerun()
            else:
                st.session_state.msg=("error","Invalid Credentials")
                st.session_state.msg_time=time.time()
                st.rerun()

        if st.button("Not registered? Register", key="hosp_signup"):
            st.session_state.signup_role="hospital"
            st.session_state.page="signup"
            st.rerun()

    with col2:
        st.markdown("### 🧑 Patient Login")

        pid = st.text_input("Patient Username", key="pat_user")
        ppass = st.text_input("Patient Password", type="password", key="pat_pass")

        if st.button("LOGIN", key="pat_login"):
            if patient_login(pid, ppass):
                st.session_state.pid = pid
                st.session_state.page = "patient_dashboard"
                st.session_state.login_time = time.time()
                st.rerun()
            else:
                st.session_state.msg=("error","Invalid Credentials")
                st.session_state.msg_time=time.time()
                st.rerun()

        if st.button("Not registered? Register", key="pat_signup"):
            st.session_state.signup_role="patient"
            st.session_state.page="signup"
            st.rerun()

# ---------------- SIGNUP ----------------
elif st.session_state.page == "signup":

    st.markdown("<h2 style='text-align:center;'>Register</h2>", unsafe_allow_html=True)
    st.divider()

    role = st.radio("Select Registration Type", ["Hospital","Patient"],
                    index=0 if st.session_state.get("signup_role")=="hospital" else 1)

    if role=="Hospital":
        st.subheader("🏥 Hospital Registration")

        hname=st.text_input("Hospital Name")
        location=st.text_input("Location")
        email=st.text_input("Hospital Email ID")
        username=st.text_input("Username")
        password=st.text_input("Password",type="password")
        confirm=st.text_input("Confirm Password",type="password")

        if st.button("REGISTER"):
            if password!=confirm:
                st.session_state.msg=("error","Passwords do not match")
            else:
                res=hospital_register(username,password,hname,location,email,"General")
                st.session_state.msg=("success","Hospital Registered") if res!="exists" else ("error","Hospital exists")
                st.session_state.page="main"

            st.session_state.msg_time=time.time()
            st.rerun()

    else:
        st.subheader("🧑 Patient Registration")

        name=st.text_input("Name")
        father=st.text_input("Father Name")
        blood=st.text_input("Blood Group")
        dob=st.text_input("DOB")
        gender=st.selectbox("Gender",["M","F"])
        phone=st.text_input("Phone")
        email=st.text_input("Email")
        username=st.text_input("Username")
        password=st.text_input("Password",type="password")
        confirm=st.text_input("Confirm Password",type="password")

        if st.button("REGISTER"):
            if password!=confirm:
                st.session_state.msg=("error","Passwords do not match")
            else:
                res=patient_register(username,password,name,0,gender,phone,father,blood,dob,email)
                st.session_state.msg=("success","Patient Registered") if res!="exists" else ("error","User exists")
                st.session_state.page="main"

            st.session_state.msg_time=time.time()
            st.rerun()

# ---------------- PATIENT DASHBOARD ----------------
elif st.session_state.page == "patient_dashboard":

    st.markdown("## 🧑 Patient Dashboard")
    st.caption(f"⏳ Auto logout in {remaining//60}m {remaining%60}s")

    if st.button("📜 Medical History"):
        st.session_state.page="patient_history"
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ---------------- PATIENT HISTORY ----------------
elif st.session_state.page == "patient_history":

    st.markdown("## 📜 Medical History")

    if st.button("⬅ Back"):
        st.session_state.page="patient_dashboard"
        st.rerun()

    pid=st.session_state.get("pid")

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("""
    SELECT h.name,h.location,a.date,t.amount,
           a.notes,a.prescription,a.diagnosis,a.symptoms,a.tests,a.advice
    FROM appointments a
    JOIN hospitals h ON a.hospital_id=h.hospital_id
    JOIN transactions t ON a.id=t.appointment_id
    WHERE a.patient_id=?
    """,(pid,))

    data=cur.fetchall()
    con.close()

    if not data:
        st.warning("No medical history found")

    for row in data:
        with st.container(border=True):
            st.markdown(f"**🏥 {row[0]}**")
            st.write(f"📍 {row[1]}")
            st.write(f"📅 {row[2]}")
            st.write(f"💰 ₹{row[3]}")
            st.write(f"📝 {row[4]}")
            st.write(f"💊 {row[5]}")
            st.write(f"🧠 {row[6]}")
            st.write(f"🤒 {row[7]}")
            st.write(f"🧪 {row[8]}")
            st.write(f"📋 {row[9]}")

    if data:
        pdf=generate_pdf(data)
        st.download_button("Download PDF",pdf,"report.pdf")

# ---------------- HOSPITAL DASHBOARD ----------------
elif st.session_state.page == "hospital_dashboard":

    st.markdown("## 🏥 Hospital Dashboard")

    # ✅ SHOW AUTO LOGOUT TIMER
    st.caption(f"⏳ Auto logout in {remaining//60} min {remaining%60} sec")

    if st.button("📝 Update Record"):
        st.session_state.page="update_record"
        st.rerun()

    if st.button("📜 View Patient History"):
        st.session_state.page="view_patient_history"
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
# ---------------- UPDATE RECORD ----------------
elif st.session_state.page == "update_record":

    st.markdown("## 📝 Update Record")

    if st.button("⬅ Back"):
        st.session_state.page="hospital_dashboard"
        st.rerun()

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("SELECT patient_id FROM patients")
    patients=[p[0] for p in cur.fetchall()]

    selected=st.selectbox("Select Patient",patients)

    category=st.selectbox("Medical Category",
        ["Routine","BP","MRI","Surgery","Diabetes","Chest Pain","Physio","Neuro","Cardiac","Ortho"]
    )

    symptoms=st.text_area("Symptoms")
    diagnosis=st.text_area("Diagnosis")
    prescription=st.text_input("Prescription")
    tests=st.text_input("Tests")
    advice=st.text_area("Advice")
    note=st.text_area("Doctor Notes")

    if st.button("Submit"):

        cur.execute("""
        INSERT INTO appointments(
            patient_id,hospital_id,date,notes,
            prescription,diagnosis,symptoms,tests,advice
        )
        VALUES(?,?,DATE('now'),?,?,?,?,?,?)
        """,(selected,st.session_state.hid,f"{category}: {note}",
             prescription,diagnosis,symptoms,tests,advice))

        appointment_id=cur.lastrowid

        cur.execute("""
        INSERT INTO transactions(appointment_id,amount,status)
        VALUES(?,?,?)
        """,(appointment_id,500,"PAID"))

        con.commit()
        con.close()

        st.session_state.msg=("success","Record Updated")
        st.session_state.msg_time=time.time()
        st.session_state.page="hospital_dashboard"
        st.rerun()

# ---------------- VIEW PATIENT HISTORY ----------------
elif st.session_state.page == "view_patient_history":

    st.markdown("## 📜 Patient History")

    if st.button("⬅ Back"):
        st.session_state.page="hospital_dashboard"
        st.rerun()

    # 🔥 SESSION STORAGE
    if "history_data" not in st.session_state:
        st.session_state.history_data = None

    if "patient_info" not in st.session_state:
        st.session_state.patient_info = None

    pid = st.text_input("Enter Patient ID")

    if st.button("Load"):

        con = sqlite3.connect(DB)
        cur = con.cursor()

        # Patient details
        cur.execute("""
        SELECT name,father,blood,dob,gender,phone,email
        FROM patients
        WHERE patient_id=?
        """,(pid,))
        st.session_state.patient_info = cur.fetchone()

        # History
        cur.execute("""
        SELECT h.name,h.location,a.date,t.amount,
               a.notes,a.prescription,a.diagnosis,a.symptoms,a.tests,a.advice
        FROM appointments a
        JOIN hospitals h ON a.hospital_id=h.hospital_id
        JOIN transactions t ON a.id=t.appointment_id
        WHERE a.patient_id=?
        ORDER BY a.date DESC
        """,(pid,))

        st.session_state.history_data = cur.fetchall()

        con.close()

    # 🔥 DISPLAY (PERSISTED)
    if st.session_state.patient_info:

        p = st.session_state.patient_info

        st.markdown("### 👤 Patient Details")
        with st.container(border=True):
            st.write(f"🆔 ID: {pid}")
            st.write(f"👤 Name: {p[0]}")
            st.write(f"👨 Father: {p[1]}")
            st.write(f"🩸 Blood Group: {p[2]}")
            st.write(f"🎂 DOB: {p[3]}")
            st.write(f"⚧ Gender: {p[4]}")
            st.write(f"📞 Phone: {p[5]}")
            st.write(f"📧 Email: {p[6]}")

    if st.session_state.history_data:

        for row in st.session_state.history_data:
            with st.container(border=True):
                st.markdown(f"**🏥 {row[0]}**")
                st.write(f"📍 {row[1]}")
                st.write(f"📅 {row[2]}")
                st.write(f"💰 ₹{row[3]}")
                st.write(f"📝 {row[4]}")
                st.write(f"💊 {row[5]}")
                st.write(f"🧠 {row[6]}")
                st.write(f"🤒 {row[7]}")
                st.write(f"🧪 {row[8]}")
                st.write(f"📋 {row[9]}")

        # ✅ PDF
        pdf = generate_pdf(st.session_state.history_data)
        st.download_button("📄 Download PDF", pdf, "report.pdf")

    elif st.session_state.history_data == []:
        st.warning("No records found")