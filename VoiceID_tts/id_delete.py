"""
voiceID_tts_test.py 실행 후 생성된 voice ID를 삭제하는 파일. (최신의 voice ID 삭제)
"""
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv
app = Flask(__name__)


load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")

def get_voice_list():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        voices = response.json().get('voices', [])
        print("Voice List:")
        for voice in voices:
            print(f"- Voice ID: {voice['voice_id']}, Name: {voice['name']}")
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        
def get_voice_id_by_name(name):
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        voices = response.json().get('voices', [])
        for voice in voices:
            if voice['name'] == name:
                return voice['voice_id']
        print(f"No voice found with the name: {name}")
        return None
    else:
        print(f"Failed to retrieve voices. Status Code: {response.status_code}, Response: {response.json()}")
        return None

def delete_voice(voice_id):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {"xi-api-key": API_KEY}

    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Voice ID {voice_id} deleted successfully.")
    else:
        print(f"Failed to delete Voice ID {voice_id}.")
        print(f"Status Code: {response.status_code}, Response: {response.json()}")


if __name__ == '__main__':
    voice_name_to_delete = "My Custom Voice"  # 삭제하려는 Voice의 이름
    voice_id = get_voice_id_by_name(voice_name_to_delete)
    if voice_id:
        delete_voice(voice_id)