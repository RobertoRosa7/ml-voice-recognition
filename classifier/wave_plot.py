import os
import wave
import numpy as np
import matplotlib.pyplot as plt

PATH_AUDIO_TEST = os.path.join('..', 'test')

obj = wave.open(os.path.join(PATH_AUDIO_TEST, 'stop.wav'), 'rb')
sample_freq = obj.getframerate()
n_samples = obj.getnframes()
signal_wave = obj.readframes(-1)

obj.close()

t_audio =  n_samples / sample_freq
print(f'Time Audio: {t_audio} seconds')

signal_array = np.frombuffer(signal_wave, dtype=np.int16)

times = np.linspace(0, t_audio, num=n_samples)

plt.figure(figsize=(15, 5))
plt.plot(times, signal_array)
plt.title("Audio Signal")
plt.ylabel("Signal Wave")
plt.xlabel("Time (seconds)")
plt.xlim(0, t_audio)
plt.show()