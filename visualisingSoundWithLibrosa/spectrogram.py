import librosa
import matplotlib.pyplot as plt
import numpy as np

audioPath = "visualiserTwo/Files/lonelyGirl.wav"
y, sr = librosa.load(audioPath)

#standard fourier transform to get the frequencies and their amplitudes at each time step
stft = librosa.stft(y)
#Convert complex STFT to magnitude
S = np.abs(stft)

#Plot spectrogram
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram (dB)')
plt.tight_layout()
plt.show()