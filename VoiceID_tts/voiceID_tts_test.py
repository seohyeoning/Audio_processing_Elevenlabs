"""실행방법: python voiceID_tts_test.py
"""
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from flask import render_template

# .env 파일 로드
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('voice_id.html')


@app.route('/generate_voice_id', methods=['POST'])
def generate_voice_id():
    file = request.files['file']
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {"xi-api-key": API_KEY}
    files = {'files': file}
    data = {'name': 'My Custom Voice'}

    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        result = response.json()
        voice_id = result.get('voice_id')
        if voice_id:
            return jsonify({"message": "Voice ID generated successfully", "voice_id": voice_id})
        else:
            return jsonify({"error": "Voice ID not found in response"}), 500
    else:
        return jsonify({"error": response.json()}), response.status_code
    
    

# Route to generate speech from text
@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    data = request.json
    voice_id = data['voice_id']
    text = data['text']
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 1.0
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        audio_content = response.content
        return audio_content, 200, {'Content-Type': 'audio/mpeg'}
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
