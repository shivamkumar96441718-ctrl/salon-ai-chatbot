
import streamlit as st
import gspread
from groq import Groq
from google.oauth2.service_account import Credentials

# PAGE SETTINGS
st.set_page_config(
    page_title="Beauty AI Assistant",
    page_icon="💇",
    layout="centered"
)


# DARK PREMIUM DESIGN
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #090b16;
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}

h1 {
    color: #ffffff;
    font-size: 38px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #e9d5ff;
}

p, label {
    color: #cbd5e1;
}

.stChatMessage {
    background: #171a2b;
    border: 1px solid #292d45;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    background: #171a2b;
    border: 1px solid #8b5cf6;
    border-radius: 16px;
}

.stTextInput input, .stDateInput input,
.stSelectbox div[data-baseweb="select"] {
    background: #171a2b;
    color: white;
    border-radius: 12px;
}

.stButton button, .stFormSubmitButton button {
    background: linear-gradient(90deg, #7c3aed, #a855f7);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
}

.stButton button:hover, .stFormSubmitButton button:hover {
    border: 1px solid #c4b5fd;
    color: white;
    background: #6d28d9;
}

hr {
    border-color: #292d45;
}

[data-testid="stForm"] {
    background: #121526;
    padding: 22px;
    border: 1px solid #292d45;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)


# API KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are Beauty AI Assistant, a professional salon customer support chatbot.

You help customers with:
1. Haircut
2. Hair Spa
3. Facial
4. Appointment booking information

Be polite, friendly and professional.
Use simple English or Hindi according to the customer.
Never invent salon prices or opening hours.
Do not claim an appointment is confirmed.
"""

# GOOGLE SHEETS CONNECTION
def connect_google_sheet():
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    client_sheet = gspread.authorize(credentials)
    sheet = client_sheet.open_by_key("1ehgsFLsYz8lfen_ax6uK_Ww8n5EsOK_4CEXy5iUiBBc").sheet1

    return sheet


# SAVE BOOKING
def save_booking(name, phone, service, date):
    sheet = connect_google_sheet()

    sheet.append_row([
        name,
        phone,
        service,
        str(date),
        "New"
    ])


# WEBSITE DESIGN
st.title("💇 Beauty AI Assistant")
st.caption("Your Smart Salon Customer Assistant")

st.divider()

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW OLD MESSAGES
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# CHAT INPUT
user_message = st.chat_input("Ask me anything about our salon...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Beauty AI is thinking..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        }
                    ] + st.session_state.messages
                )

                answer = response.choices[0].message.content

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"AI Error: {e}")


# APPOINTMENT FORM
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
            save_booking(
                name,
                phone,
                service,
                appointment_date
            )

            st.success("Appointment request saved successfully!")

            st.write("Customer:", name)
            st.write("Customer:", phone)
            st.write("Service:", service)
            st.write("Date:", appointment_date)

            st.info("This is a request, not a confirmed appointment.")

        except Exception as e:
            st.error(f"Booking Error: {type(e).__name__}: {e}")

    else:
        st.warning("Please enter your name and phone number.")


st.divider()
st.caption("Beauty AI | Powered by Groq")
