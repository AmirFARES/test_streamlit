import streamlit as st
import requests

# Your public API URL
API_URL = "https://c0be-34-16-241-63.ngrok-free.app/generate"

# Streamlit page config
st.set_page_config(page_title="Chat with AmirGPT", page_icon="🤖")
st.title("💬 Chat with AmirGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
prompt = st.chat_input("اكتب رسالتك هنا...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the prompt to your FastAPI server
    response = requests.post(API_URL, json={"text": prompt})

    # Parse the response
    if response.status_code == 200:
        model_reply = response.json().get("response", "")
    else:
        model_reply = "❌ Error getting response."

    # Add model message to history
    st.session_state.messages.append({"role": "assistant", "content": model_reply})

    # Show model response
    with st.chat_message("assistant"):
        st.markdown(model_reply)
