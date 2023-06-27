"""
Server

Client -> Post Request -> Server -> prediction back to client
"""
import os
import base64
import wave
import pyaudio
import json

from api_communication import *
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS


AUDIO_NAME = 'temp.wav'
FRAMES_PER_BUFFER = 22050
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 16000
PATH_AUDIO_LOG = os.path.join('logs_audio')


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def get_health():
    return "Audio Recognition Machine Learning Server is up!"



@app.route("/audio-blob", methods=["POST"])
def audi_blob():
    if not os.path.exists(PATH_AUDIO_LOG):
        os.makedirs(PATH_AUDIO_LOG)

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(PATH_AUDIO_LOG, filename)
    file.save(filepath)

    data, error = get_transcript({'audio_url': get_body(filepath), 'language_code': 'pt'})

    reponse = data if error is None else 'Text not found'

    response = app.response_class(
        response=json.dumps({"keyword": reponse['text']}),
        status=200,
        mimetype='application/json'
    )

    return response



@app.route('/check-audio', methods=["POST"])
def check_audio():
    app.logger.debug("[/check-audio] => startind endpoint")

    pa = pyaudio.PyAudio()
    body = request.json
    base = body['audio'].split(',')[1]
    decodedData = base64.b64decode(base)
    frames = []

    with open(os.path.join(AUDIO_NAME), 'wb') as f:
        f.write(decodedData)
        f.close()
    
    # with open(os.path.join(AUDIO_NAME), 'rb') as f:
    #     for frame in f.readlines():
    #         frames.append(frame)
    #     f.close()
    
    obj = wave.open(AUDIO_NAME, 'rb')
    print(f'Channels: {obj.getnchannels()}')
    
    obj.close()

    # obj.setnchannels(CHANNELS)
    # obj.setsampwidth(pa.get_sample_size(FORMAT))
    # obj.setframerate(RATE)
    # obj.writeframes(b''.join(frames))
    # obj.close()

    # make a prediction
    # os.remove(os.path.join(AUDIO_NAME))


    response = app.response_class(
        response=json.dumps({"keyword": "predicted_keyword"}),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    app.run(debug=True)
