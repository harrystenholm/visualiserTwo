import librosa
import matplotlib.pyplot as plt
import numpy as np

audioPath = "visualiserTwo/Files/lonelyGirl.wav"
y, sr = librosa.load(audioPath)

#Compute MFCCs with different n_mfcc values
mfccs13 = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
mfccs40 = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

#Plot MFCCs
plt.figure(figsize=(12,6))
plt.subplot(2, 1, 1)
librosa.display.specshow(mfccs13, sr=sr, x_axis='time')
plt.colorbar()
plt.title('MFCC 13')

plt.subplot(2,1,2)
librosa.display.specshow(mfccs40, sr=sr, x_axis='time')
plt.colorbar()
plt.title('MFCC 40')

plt.tight_layout()
plt.show()