import sounddevice as sd

info = sd.query_devices()
print(sd.query_hostapis())
print(info)
