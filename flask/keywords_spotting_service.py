import numpy as np
import tensorflow.keras as keras
import os
import librosa
import json
import wave
import pyaudio

MODEL_PATH = os.path.join("model.h5")
SAMPLE_TO_CONSIDER = 22050  # 1 seconds
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 16000

pa = pyaudio.PyAudio()

class _Keywords_Spotting_Service:
    model = None
    _mappings = [
        "down",
        "off",
        "on",
        "no",
        "yes",
        "stop",
        "up",
        "right",
        "left",
        "go"
    ]
    _istance = None

    def load_dataset(self, data_path):
        with open(data_path, 'r') as fp:
            data = json.load(fp)

        # extract inputs and targets
        x = data["MFCCs"]

        return np.array(x)

    def predict(self, file_path):
        # extract MFCCs
        mfccs = self.preprocess(file_path)  # (segments, coefficients)

        # convert 2d MFCCs array into 4d array -> (sample, segments, coefficients, channels)
        # MFCCs = MFCCs[np.newaxis, ..., np.newaxis]
        mfccs = mfccs[np.newaxis, ..., np.newaxis]

        # make prediction
        predictions = self.model.predict(mfccs)  # [ [0.1, 0.6, 0.1, ...] ]
        prediction_index = np.argmax(predictions)
        
        try:
            prediction_keyword = self._mappings[prediction_index]
        except IndexError as e:
            prediction_keyword = "Not Found"
        
        return prediction_keyword

    def preprocess(self, file_path, n_mfcc=13, n_fft=2048, hop_length=512):
        # load audio file
        signal, sr = librosa.load(file_path)

        # ensure consistency in the audio file length
        if len(signal) >= SAMPLE_TO_CONSIDER:
            signal = signal[:SAMPLE_TO_CONSIDER]

        # extract MFCCs
        MFCCs = librosa.feature.mfcc(y=signal, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=n_fft)

        return np.array(MFCCs.T.tolist())


def Keywords_Spotting_Service():
    # ensure that we only have 1 instance of KSS
    if _Keywords_Spotting_Service._istance is None:
        _Keywords_Spotting_Service._istance = _Keywords_Spotting_Service()
        _Keywords_Spotting_Service.model = keras.models.load_model(MODEL_PATH)

    return _Keywords_Spotting_Service._istance


if __name__ == "__main__":
    kss = Keywords_Spotting_Service()
    frames = []

    with open(os.path.join('down.wav'), 'rb') as f:
        for frame in f.readlines():
            frames.append(frame)
        f.close()

    
    obj = wave.open('test.wav', 'wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(pa.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b''.join(frames))
    obj.close()

    predict = kss.predict(os.path.join('test.wav'))
    print(f'Predict word: {predict}')
