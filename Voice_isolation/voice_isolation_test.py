"""실행방법: streamlit run voice_isolation_test.py
"""
import streamlit as st
import requests
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
import requests

# .env 파일 로드
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


def process_audio(audio_file):
    url = "https://api.elevenlabs.io/v1/audio-isolation/stream"
    

    files = {"audio": audio_file}
    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"API Error: {response.status_code} - {response.text}")
        return None

# Streamlit UI
st.title("ElevenLabs Real-Time Audio Isolation Chatbot")

# 채팅과 유사한 작동이 이루어지도록 session_state 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.subheader("Chat with Real-Time Audio")

duration = st.slider("Recording duration (seconds)", 1, 10, 5, key="chat_duration")
if st.button("Record and Send Audio", key="send_audio"):
    with st.spinner("Recording..."):
        fs = 44100  
        st.info("Recording started...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  
        st.success("Recording completed!")

        # 녹음된 오디오와 temp 파일 저장  
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            write(temp_audio.name, fs, audio_data)
            temp_audio_path = temp_audio.name

        # 오디오 처리
        with open(temp_audio_path, "rb") as audio_file:
            processed_audio = process_audio(audio_file)

        if processed_audio:
            # session state 저장
            st.session_state["messages"].append({
                "type": "user",
                "audio": temp_audio_path
            })
            st.session_state["messages"].append({
                "type": "bot",
                "audio": processed_audio
            })

# 채팅 메시지 보이기
for message in st.session_state["messages"]:
    if message["type"] == "user":
        st.subheader("You:")
        st.audio(message["audio"], format="audio/wav")
    elif message["type"] == "bot":
        st.subheader("Bot:")
        st.audio(message["audio"], format="audio/wav")