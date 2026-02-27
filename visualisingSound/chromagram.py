import librosa
import matplotlib.pyplot as plt
import numpy as np

audioPath = "visualiserTwo/Files/lonelyGirl.wav"
y, sr = librosa.load(audioPath)

#standard fourier transform to get the frequencies and their amplitudes at each time step
stft = librosa.stft(y)
#Convert complex STFT to magnitude
S = np.abs(stft)
#Convert to dB
S_db = librosa.amplitude_to_db(S, ref=np.max)

#Plot spectrogram with high freq resolution
plt.figure(figsize=(12,6))
plt.subplot(4,1,1)
librosa.display.specshow(S_db, sr=sr,x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram with High Frequency Resolution')

# Harmonic-Percussive Source Separation (HPSS)
harmonic, percussive = librosa.effects.hpss(y)

#Compute and plot harmonic spectrogram
D_harmonic = librosa.stft(harmonic, n_fft=4096)
S_harmonic = np.abs(D_harmonic)
S_harmonic_db = librosa.amplitude_to_db(S_harmonic, ref = np.max)

plt.subplot(4,1,2)
librosa.display.specshow(S_harmonic_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Harmonic Spectrogram')


# Compute and plot percussive spectrogram
D_percussive = librosa.stft(percussive, n_fft=4096)
S_percussive = np.abs(D_percussive)
S_percussive_db = librosa.amplitude_to_db(S_percussive, ref=np.max)

plt.subplot(4,1,3)
librosa.display.specshow(S_percussive_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Percussive Spectrogram')

#Compute and plot chromagram
chromagram = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=4906, n_chroma=24)

plt.subplot(4,1,4)
librosa.display.specshow(chromagram,sr=sr, x_axis='time', y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')

plt.tight_layout()
plt.show()

