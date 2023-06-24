"""
Server

Client -> Post Request -> Server -> prediction back to client
"""
import os
import random
from flask import Flask, request, jsonify
from keywords_spotting_service import Keywords_Spotting_Service
import base64
import wave
import pyaudio
import json

AUDIO_NAME = 'temp.webm'
FRAMES_PER_BUFFER = 22050
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 16000


app = Flask(__name__)

"""
ks.com/predict
"""

@app.route("/", methods=["GET"])
def get_health():
    return "Audio Recognition Machine Learning Server is up!"


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
    
    # obj = wave.open(AUDIO_NAME, 'wb')
    # obj.setnchannels(CHANNELS)
    # obj.setsampwidth(pa.get_sample_size(FORMAT))
    # obj.setframerate(RATE)
    # obj.writeframes(b''.join(frames))
    # obj.close()

    kss = Keywords_Spotting_Service()

    # make a prediction
    predicted_keyword = kss.predict(os.path.join(AUDIO_NAME))

    # os.remove(os.path.join(AUDIO_NAME))

    app.logger.debug(f"[/check-audio] => predict word: {predicted_keyword}")

    response = app.response_class(
        response=json.dumps({"keyword": predicted_keyword}),
        status=200,
        mimetype='application/json'
    )

    return response



@app.route("/predict", methods=["POST"])
def predict():
    # get audio file and save it
    audio_file = request.files["file"]
    file_name = str(random.randint(0, 100000))
    audio_file.save(file_name)

    # invoke keyword spotting service
    kss = Keywords_Spotting_Service()

    # make a prediction
    predicted_keyword = kss.predict(file_name)

    # remove audio file
    os.remove(file_name)

    # send back the predicted keyword in json format
    data = {"keyword": predicted_keyword}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
