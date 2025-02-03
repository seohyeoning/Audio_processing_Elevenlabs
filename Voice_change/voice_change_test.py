"""실행방법: streamlit run voice_change_test.py
"""
import streamlit as st
import requests
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv
import requests

# .env 파일 로드
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


if not ELEVENLABS_API_KEY:
    st.error("API key is missing. Please set the ELEVENLABS_API_KEY environment variable.")
    st.stop()


VOICE_ID = "Enter your voice id"  # Voice ID
MODEL_ID = "eleven_multilingual_sts_v2"  # Model ID

# 오디오 처리 함수
def process_audio(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            # API 요청
            response = requests.post(
                f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICE_ID}/stream",
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                },
                files={"audio": audio_file},
                data={"model_id": MODEL_ID},
            )

            # 응답 상태 확인
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}, {response.json()}")
                return None

            # 스트림 데이터를 로컬 파일로 저장
            output_audio_path = tempfile.mktemp(suffix=".mp3")
            with open(output_audio_path, "wb") as f:
                f.write(response.content)

            return output_audio_path
    except Exception as e:
        st.error(f"Error during processing: {e}")
        return None

# Streamlit UI
st.title("ElevenLabs Real-Time Voice Changer Chatbot")

# Chat-like interface
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.subheader("Chat with Real-Time Audio")

# 녹음 길이 슬라이더
duration = st.slider("Recording duration (seconds)", 1, 10, 5, key="chat_duration")

# 녹음 및 전송 버튼
if st.button("Record and Send Audio", key="send_audio"):
    with st.spinner("Recording..."):
        fs = 44100  
        st.info("Recording started...")
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait() 
        st.success("Recording completed!")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            write(temp_audio.name, fs, audio_data)
            temp_audio_path = temp_audio.name

        processed_audio = process_audio(temp_audio_path)

        if processed_audio:
            st.session_state["messages"].append({
                "type": "user",
                "audio": temp_audio_path
            })
            st.session_state["messages"].append({
                "type": "bot",
                "audio": processed_audio
            })

# 챗 메시지 보이기
for message in st.session_state["messages"]:
    if message["type"] == "user":
        st.subheader("You:")
        st.audio(message["audio"], format="audio/wav")
    elif message["type"] == "bot":
        st.subheader("Bot:")
        st.audio(message["audio"], format="audio/wav")