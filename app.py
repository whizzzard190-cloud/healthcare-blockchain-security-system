import streamlit as st
import sqlite3
from auth.auth_system import patient_login, patient_register, hospital_login

DB="database/healthcare.db"

st.set_page_config(page_title="Blockchain Healthcare",layout="centered")

st.markdown("<h1 style='text-align:center'>🏥 Blockchain Healthcare Security System</h1>",unsafe_allow_html=True)
st.divider()

menu=st.sidebar.selectbox(
    "Select Role",
    ["Patient Login","Patient Signup","Hospital Login"],
    key="role_menu"
)

# ---------------- PATIENT SIGNUP ----------------
if menu=="Patient Signup":

    st.subheader("🧑 Patient Registration")

    pid=st.text_input("Patient ID")
    password=st.text_input("Password",type="password")
    name=st.text_input("Full Name")
    age=st.number_input("Age",min_value=1)
    gender=st.selectbox("Gender",["M","F"])
    phone=st.text_input("Phone")

    if st.button("Register"):
        patient_register(pid,password,name,age,gender,phone)
        st.success("Patient Registered Successfully")

# ---------------- PATIENT LOGIN ----------------
if menu=="Patient Login":

    st.subheader("🧑 Patient Login")

    pid=st.text_input("Patient ID")
    password=st.text_input("Password",type="password")

    if st.button("Login"):
        user=patient_login(pid,password)

        if user:
            st.success("Login Successful")

            con=sqlite3.connect(DB)
            cur=con.cursor()

            # ✅ ORDER BY DATE so updated visit appears first
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

            st.subheader("📜 Medical History")

            for row in data:
                with st.container(border=True):
                    st.write("🏥 Hospital:",row[0])
                    st.write("📍 Location:",row[1])
                    st.write("📅 Date:",row[2])
                    st.write("💰 Amount (₹):",row[3])
                    st.write("📝 Notes:",row[4])

        else:
            st.error("Invalid Credentials")

# ---------------- HOSPITAL LOGIN ----------------
if menu=="Hospital Login":

    st.subheader("🏥 Hospital Dashboard")

    if "hosp_logged" not in st.session_state:
        st.session_state.hosp_logged=False

    if not st.session_state.hosp_logged:

        hid=st.text_input("Hospital ID")
        password=st.text_input("Password",type="password")

        if st.button("Login"):
            hosp=hospital_login(hid,password)

            if hosp:
                st.session_state.hosp_logged=True
                st.session_state.hid=hid
                st.rerun()
            else:
                st.error("Invalid Credentials")

    else:

        hid=st.session_state.hid

        con=sqlite3.connect(DB)
        cur=con.cursor()

        cur.execute("SELECT DISTINCT patient_id FROM appointments WHERE hospital_id=?",(hid,))
        patients=[p[0] for p in cur.fetchall()]

        if patients:

            selected=st.selectbox("Select Patient",patients)

            category=st.selectbox(
                "Medical Category",
                ["Routine","BP","MRI","Surgery","Diabetes","Chest Pain","Physio","Neuro","Cardiac","Ortho"]
            )

            personal_note=st.text_area("Doctor Personal Notes")

            col1,col2=st.columns(2)

            with col1:
                if st.button("✅ Update Latest Visit"):

                    final_note=f"{category}: {personal_note}"

                    cur.execute("""
                    UPDATE appointments
                    SET notes=?
                    WHERE id = (
                        SELECT id FROM appointments
                        WHERE patient_id=? AND hospital_id=?
                        ORDER BY id DESC LIMIT 1
                    )
                    """,(final_note,selected,hid))

                    con.commit()
                    con.close()

                    st.success("Latest Medical Record Updated")
                    st.rerun()

            with col2:
                if st.button("🚪 Logout"):
                    st.session_state.hosp_logged=False
                    st.rerun()

        con.close()
