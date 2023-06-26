import os
from pydub import AudioSegment
PATH_AUDIO_TEST = os.path.join('..', 'test')
PATH_AUDIO_FILE = os.path.join(PATH_AUDIO_TEST, 'stop.wav')
PATH_AUDIO_FILE_MP3 = os.path.join(PATH_AUDIO_TEST, 'mashup.mp3')

audio = AudioSegment.from_wav(PATH_AUDIO_FILE)
audio = audio + 6  # increase the volume by 6dB
audio = audio * 2
audio = audio.fade_in(2000)
audio.export(os.path.join(PATH_AUDIO_FILE_MP3), format="mp3")

audio2 = AudioSegment.from_mp3(PATH_AUDIO_FILE_MP3)
print("done")