import os
import requests

URL = "http://localhost:5000"

TEST_AUDIO_FILE_PATH = os.path.join("test", "stop.wav")

if __name__ == "__main__":
    audio_file = open(TEST_AUDIO_FILE_PATH, "rb")
    values = {"file": (TEST_AUDIO_FILE_PATH, audio_file, "audio/wav")}
    response = requests.post(URL + "/predict", files=values)

    print(response.status_code)

    data = response.json()

    print(f"Predicted Keywords is: {data['keyword']}")
