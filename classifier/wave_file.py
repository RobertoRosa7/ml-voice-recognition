# audio file formats
# .mp3
# .flac
# .wav
import os
import wave

# Audio Signal Parameters
# - number of channels
# - sample width
# - frameter/sample_rate: 44.100 Hz
# - number of frames
# - values of a frame

PATH_AUDIO_TEST = os.path.join('..', 'test')

def init():
    obj = wave.open(os.path.join(PATH_AUDIO_TEST, 'stop.wav'), 'rb')
    
    print(f'Number of channels: {obj.getnchannels()}')
    print(f'Sample width: {obj.getsampwidth()}')
    print(f'Frame Rate: {obj.getframerate()}')
    print(f'Number of frames: {obj.getnframes()}')
    print(f'Parameters: {obj.getparams()}')

    time_audio = obj.getnframes() / obj.getframerate()
    print(f'Time Audio: {time_audio} seconds')

    frames = obj.readframes(-1)
    print(f'Type frames: {type(frames)} - type frame[0]: {type(frames[0])}')
    print(f'Frame size: {len(frames)}')
    print(f'Frame size / channel: {len(frames) / 2}')

    obj.close()

    obj_new = wave.open(os.path.join(PATH_AUDIO_TEST, 'test.wav'), 'wb')
    obj_new.setnchannels(1)
    obj_new.setsampwidth(2)
    obj_new.setframerate(16000.0)
    obj_new.writeframes(frames)

    obj_new.close()

if __name__ == '__main__':
    init()

