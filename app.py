import streamlit as st
import google.generativeai as genai
import requests 

GOOGLE_API_KEY = "AIzaSyDAa0CYGO1SYZB_zPqxPuuAQW2Ez_L8vWY"
ELEVENLABS_API_KEY = "sk_0bce5119b19797b08a5d606d490744dd16bda9c611ced2b6"

st.set_page_config(page_title="SAvant", page_icon="🤖")
st.title("SAvant AI Interviewer")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "model", "parts": ["Hello, I am SAvant. I am here to interview you. Please introduce yourself."]})

for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    st.chat_message(role).write(msg["parts"][0])

user_input = st.chat_input("Type your answer here...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "parts": [user_input]})

    try:
        chat = model.start_chat(history=st.session_state.messages)
        response = chat.send_message(user_input)
        ai_reply = response.text
        
        st.chat_message("assistant").write(ai_reply)
        st.session_state.messages.append({"role": "model", "parts": [ai_reply]})

        voice_id = "21m00Tcm4TlvDq8ikWAM"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": ai_reply,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        audio_res = requests.post(url, json=data, headers=headers)
        if audio_res.status_code == 200:
            st.audio(audio_res.content, format="audio/mp3", autoplay=True)
            
    except Exception as e:
        st.error(f"Error: {e}")
