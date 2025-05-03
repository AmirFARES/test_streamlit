import streamlit as st
import requests

# Hugging Face Inference API URL
API_URL = "https://0228-34-125-224-246.ngrok-free.app/generate"
HF_API_TOKEN = "your_huggingface_token"  # Optional: leave "" if model is public

# Streamlit page config
st.set_page_config(page_title="الدردشة مع نموذج جيس", page_icon="🤖")
st.title(f"💬 الدردشة مع نموذج جيس")

# Arabic system prompt (Customer Support style)
SYSTEM_PROMPT = """
أنت مساعد ذكي يتحدث اللغة العربية ومهمتك هي تقديم دعم عملاء احترافي.
كن ودودًا، واضحًا، وساعد المستخدمين بأفضل شكل ممكن.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("اكتب رسالتك هنا...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Combine system prompt + chat history
    full_prompt = f"تعليمات النظام: {SYSTEM_PROMPT.strip()}\n"
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            full_prompt += f"المستخدم: {msg['content']}\n"
        elif msg["role"] == "assistant":
            full_prompt += f"المساعد: {msg['content']}\n"
    full_prompt += "المساعد:"

    # Prepare headers and payload
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}
    payload = {"inputs": full_prompt}

    # Call HF API
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            output = response.json()
            generated_text = output[0]["generated_text"]
            model_reply = generated_text[len(full_prompt):].strip()
        else:
            model_reply = "❌ حدث خطأ أثناء الاتصال بالنموذج."
    except Exception as e:
        model_reply = f"❌ فشل الاتصال بالنموذج: {e}"

    # Save and display assistant reply
    st.session_state.messages.append({"role": "assistant", "content": model_reply})
    with st.chat_message("assistant"):
        st.markdown(model_reply)
