import librosa
import matplotlib.pyplot as plt
import numpy as np

audioPath = "visualiserTwo/Files/lonelyGirl.wav"
y, sr = librosa.load(audioPath)

#standard fourier transform to get the frequencies and their amplitudes at each time step
stft = librosa.stft(y)

#find maximum amplitude across frequencies for each time step
amplitude_envelope = np.max(np.abs(stft), axis = 0)

#initialise main plot
plt.figure(figsize=(12, 6))

#plot waveform
plt.subplot(3, 1, 1)
librosa.display.waveshow(y, sr=sr, alpha = 0.5)
plt.title("waveform")

#plot peak amplitude envelope
plt.subplot(3, 1, 2)
plt.plot(
    librosa.frames_to_time(np.arange(len(amplitude_envelope)), sr =sr), 
    amplitude_envelope, label = 'Max Amplitude'
)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title("Peak Amplitude Envelope")
plt.legend()

#plot onset times as vertical lines
plt.subplot(3 ,1 ,3)
onset_time = onset_time = librosa.onset.onset_detect(y=y, sr=sr, units='time')
librosa.display.waveshow(y, sr=sr, alpha = 0.5)
plt.vlines(onset_time, -1, 1, color='g', linestyle='dashed', label="Onsets")
plt.legend()
plt.title('Onset Direction')

plt.tight_layout()
plt.show()
