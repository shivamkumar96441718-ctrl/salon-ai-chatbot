
import streamlit as st
from groq import Groq

import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="Beauty AI Assistant",
    page_icon="✨",
    layout="wide"
)
st.write("Available Secret Names:", list(st.secrets.keys()))
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10101e, #211536);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #6938b5, #30204f);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
}
.info-card {
    background: #29213c;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #51406e;
    min-height: 125px;
}
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """
You are Beauty AI, a professional salon customer support assistant.

Available services:
1. Haircut
2. Hair Spa
3. Facial

Prices, location and opening hours are not provided.

Rules:
- Speak politely and naturally.
- Answer in the customer's language.
- Never invent prices or timings.
- Help customers understand services and booking.
"""

st.markdown("""
<div class="hero">
<h1>✨ Beauty AI Assistant</h1>
<p>Your Personal Salon Support Assistant</p>
<p>🤖 Powered by Groq AI</p>
</div>
""", unsafe_allow_html=True)

st.subheader("💎 Our Premium Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
    <h3>✂️ Haircut</h3>
    <p>Professional haircut services.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
    <h3>💆 Hair Spa</h3>
    <p>Relaxing hair spa services.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
    <h3>✨ Facial</h3>
    <p>Personal facial care services.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("🤖 Chat With Beauty AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🔄 New Conversation"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Message Beauty AI...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        try:
            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            chat_messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + st.session_state.messages

            with st.spinner("Beauty AI is thinking..."):
                response = client.chat.completions.create(
                   model="openai/gpt-oss-120b",
                    messages=chat_messages
                )

            answer = response.choices[0].message.content
            st.markdown(answer)

 except Exception as e:
    st.exception(e)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

def connect_google_sheet():
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    client = gspread.authorize(credentials)
    sheet = client.open("Beauty AI Bookings").sheet1
    return sheet
       
def save_booking(name, phone, service, date):
    sheet = connect_google_sheet()
    sheet.append_row([
        name,
        phone,
        service,
        str(date),
        "New"
    ])

st.divider()
st.subheader("📅 Appointment Request")

with st.form("appointment_form"):
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    service = st.selectbox(
        "Select Service",
        ["Haircut", "Hair Spa", "Facial"]
    )
    appointment_date = st.date_input("Appointment Date")

    submitted = st.form_submit_button("Submit Request")

    if submitted:
        if name.strip() and phone.strip():
            try:
                save_booking(name, phone, service, appointment_date)
                st.success("Appointment request saved successfully!")
                st.write("Name:", name)
                st.write("Phone:", phone)
                st.write("Service:", service)
                st.write("Date:", appointment_date)
                st.info("This is a request, not a confirmed appointment.")

            except Exception as e:
                st.error(f"Booking save failed: {e}")

        else:
            st.warning("Please enter your name and phone number.")
