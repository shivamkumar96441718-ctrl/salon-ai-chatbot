
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Beauty Salon AI",
    page_icon="💇",
    layout="wide"
)

# Salon information
SALON_INFO = """
We provide:
1. Haircut
2. Hair Spa
3. Facial

Prices, location and opening hours are not provided.
Never invent missing information.
"""

# Website design
st.title("💇 Beauty Salon")
st.subheader("Welcome to our Beauty Salon!")
st.write("Your personal AI Salon Assistant is here to help.")

st.divider()

# Services
st.header("Our Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("✂️ Haircut")
    st.write("Professional haircut service.")

with col2:
    st.subheader("💆 Hair Spa")
    st.write("Relaxing hair spa service.")

with col3:
    st.subheader("✨ Facial")
    st.write("Facial care service.")

st.divider()

# Appointment booking
st.header("📅 Book Your Appointment")

with st.form("booking_form"):
    name = st.text_input("Your Name")
    service = st.selectbox(
        "Choose Service",
        ["Haircut", "Hair Spa", "Facial"]
    )
    appointment_date = st.date_input("Appointment Date")

    submitted = st.form_submit_button("Book Appointment")

    if submitted:
        if name.strip():
            st.success("Booking request received!")
            st.write("Customer:", name)
            st.write("Service:", service)
            st.write("Date:", appointment_date)
            st.info("This is a demo booking. No appointment has been confirmed.")
        else:
            st.error("Please enter your name.")

st.divider()

# AI Chatbot
st.header("🤖 Chat With Our AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_message = st.chat_input("Ask about our salon services...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.write(user_message)

    try:
        if st.session_state.chat is None:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            st.session_state.chat = client.chats.create(
                model="gemini-2.5-flash",
                config={
                    "system_instruction":
                    "You are a polite salon assistant. "
                    + SALON_INFO
                }
            )

        response = st.session_state.chat.send_message(
            user_message
        )

        answer = response.text

    except Exception:
        answer = (
            "Sorry, AI is temporarily unavailable. "
            "Please check the API configuration."
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)

st.caption("Beauty Salon | AI Customer Support Demo")

