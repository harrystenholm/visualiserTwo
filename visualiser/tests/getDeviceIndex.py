import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    # Look for "Stereo Mix" in the name
    print(f"Index {i}: {dev['name']}")
p.terminate()