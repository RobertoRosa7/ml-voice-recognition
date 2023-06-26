import os
import pyaudio
import wave

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
PATH_AUDIO_TEST = os.path.join('..', 'test')

def start_recording():
    p = pyaudio.PyAudio()

    print('starting recording')
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER   
    )

    seconds = 5
    frames = []
    for i in range(0, int(RATE/FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.start_stream()
    stream.close()
    p.terminate()

    obj = wave.open(os.path.join(PATH_AUDIO_TEST, 'output.wav'), 'wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close()
    print('closing recording')


if __name__ == '__main__':
    start_recording()