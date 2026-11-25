
import streamlit as st
from google import genai

# PAGE SETTINGS
st.set_page_config(
    page_title="Beauty AI Assistant",
    page_icon="✨",
    layout="wide"
)

# PREMIUM DESIGN
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
.stButton button {
    border-radius: 12px;
    border: 1px solid #9064cf;
}
</style>
""", unsafe_allow_html=True)

# SALON INFORMATION
salon_info = """
You are Beauty AI, a professional salon assistant.

Available services:
1. Haircut
2. Hair Spa
3. Facial

Prices: Not provided.
Location: Not provided.
Opening hours: Not provided.

Rules:
- Speak naturally and politely.
- Answer in the customer's language.
- Give detailed but simple answers.
- Never invent prices, locations or timings.
- Help customers with salon bookings.
"""

# HEADER
st.markdown("""
<div class="hero">
    <h1>✨ Beauty AI Assistant</h1>
    <p>Your Personal Salon Support Assistant</p>
    <p>🤖 Powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# SERVICES
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

# AI CHATBOT
st.subheader("🤖 Chat With Beauty AI")
st.caption("Ask me anything about our salon services!")

# INITIALIZE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = None

# RESET CHAT
if st.button("🔄 New Conversation"):
    st.session_state.messages = []
    st.session_state.chat = None
    st.rerun()

# QUICK QUESTIONS
st.write("**Quick Questions:**")

q1, q2, q3 = st.columns(3)

with q1:
    if st.button("Our Services"):
        st.session_state.pending_prompt = "What services do you provide?"

with q2:
    if st.button("Haircut Details"):
        st.session_state.pending_prompt = "Tell me about your haircut service."

with q3:
    if st.button("Booking Help"):
        st.session_state.pending_prompt = "How can I book an appointment?"

# SHOW CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# GET USER MESSAGE
user_message = st.chat_input("Message Beauty AI...")

if "pending_prompt" in st.session_state:
    user_message = st.session_state.pop("pending_prompt")

# SEND TO GEMINI
if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):

        try:
            if st.session_state.chat is None:

                api_key = st.secrets["GEMINI_API_KEY"]

                client = genai.Client(
                    api_key=api_key
                )

                st.session_state.chat = client.chats.create(
                    model="gemini-2.5-flash",
                    config={
                        "system_instruction": salon_info
                    }
                )

            with st.spinner("Beauty AI is thinking..."):

                response = st.session_state.chat.send_message(
                    user_message
                )

                answer = response.text

            st.markdown(answer)

        except Exception as e:
            answer = (
                "Sorry, I could not connect to AI right now. "
                "Please check the API settings and try again."
            )
            st.error(answer)
            st.caption(str(e))

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

st.divider()

# APPOINTMENT SECTION
st.subheader("📅 Appointment Request")

with st.form("appointment_form"):

    customer_name = st.text_input("Customer Name")

    service = st.selectbox(
        "Select Service",
        ["Haircut", "Hair Spa", "Facial"]
    )

    appointment_date = st.date_input(
        "Select Appointment Date"
    )

    submit = st.form_submit_button(
        "Submit Appointment Request"
    )

    if submit:

        if customer_name.strip():

            st.success(
                f"Demo request received for {customer_name}!"
            )

            st.write("Service:", service)
            st.write("Date:", appointment_date)

            st.info(
                "This is a demo request, not a confirmed appointment."
            )

        else:
            st.warning("Please enter your name.")

st.caption("Beauty AI | Powered by Gemini")
