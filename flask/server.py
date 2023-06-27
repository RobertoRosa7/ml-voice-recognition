"""
Server

Client -> Post Request -> Server -> prediction back to client
"""
import os
import json

from api_communication import *
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
