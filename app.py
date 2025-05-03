import streamlit as st
import requests

# Your public API URL (make sure this connects to Jais)
API_URL = "https://c0be-34-16-241-63.ngrok-free.app/generate"

# System prompt in Arabic for a customer support assistant
SYSTEM_PROMPT = "أنت مساعد دعم عملاء ودود وسريع الاستجابة من شركة جيس. ساعد المستخدمين في حل مشاكلهم بكفاءة ولباقة."

# Streamlit page config
st.set_page_config(page_title="محادثة مع نموذج جيس", page_icon="🤖")
st.title("💬 محادثة مع نموذج جيس")

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
    # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Format prompt for the API including system and full chat history
    formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    # Send the conversation to the API
    response = requests.post(API_URL, json={"messages": formatted_messages})

    # Parse the response
    if response.status_code == 200:
        model_reply = response.json().get("response", "")
    else:
        model_reply = "❌ حدث خطأ أثناء الحصول على رد من جيس."

    # Add assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": model_reply})

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(model_reply)
