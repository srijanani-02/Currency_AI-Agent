import streamlit as st
from router import router

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="💱 Currency Converter AI Agent",
    page_icon="💱",
    layout="centered"
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("💱 Currency Converter AI Agent")
    st.write("Convert currencies instantly with live exchange rates.")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main Title
# -----------------------------
st.title("💱 Currency Converter AI Agent")
st.caption("Convert currencies instantly with real-time exchange rates.")

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)

# -----------------------------
# User Input
# -----------------------------
question = st.chat_input("Ask me to convert currencies...")

if question:

    # Display user message
    st.session_state.messages.append(("user", question))

    with st.chat_message("user"):
        st.write(question)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Converting..."):
            answer = router(question)

        st.write(answer)

    st.session_state.messages.append(("assistant", answer))