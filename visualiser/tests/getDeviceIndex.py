import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(i, info['name'],
          'max in', info['maxInputChannels'],
          'rate', int(info.get('defaultSampleRate', 44100)))
    
#0 Microsoft Sound Mapper - Input max in 2 max out 0
# 1 Stereo Mix (Realtek High Defini max in 2 max out 0
# 2 Microsoft Sound Mapper - Output max in 0 max out 2
# 3 CQ27G2S (NVIDIA High Definition max in 0 max out 2
# 4 Speakers (Steam Streaming Micro max in 0 max out 8
# 5 Realtek Digital Output (Realtek max in 0 max out 2
# 6 Speakers (Steam Streaming Speak max in 0 max out 8
# 7 Primary Sound Capture Driver max in 2 max out 0
# 8 Stereo Mix (Realtek High Definition Audio) max in 2 max out 0
# 9 Primary Sound Driver max in 0 max out 2
# 10 CQ27G2S (NVIDIA High Definition Audio) max in 0 max out 2
# 11 Speakers (Steam Streaming Microphone) max in 0 max out 8
# 12 Realtek Digital Output (Realtek High Definition Audio) max in 0 max out 2
# 13 Speakers (Steam Streaming Speakers) max in 0 max out 8
# 14 CQ27G2S (NVIDIA High Definition Audio) max in 0 max out 2
# 15 Speakers (Steam Streaming Microphone) max in 0 max out 2
# 16 Realtek Digital Output (Realtek High Definition Audio) max in 0 max out 2
# 17 Speakers (Steam Streaming Speakers) max in 0 max out 2
# 18 Stereo Mix (Realtek High Definition Audio) max in 2 max out 0
# 19 Headphones (Realtek HD Audio 2nd output) max in 0 max out 2
# 20 Microphone (Realtek HD Audio Mic input) max in 2 max out 0
# 21 Stereo Mix (Realtek HD Audio Stereo input) max in 2 max out 0
# 22 SPDIF Out (Realtek HDA SPDIF Out) max in 0 max out 2
# 23 Speakers (Realtek HD Audio output) max in 0 max out 8
# 24 Line In (Realtek HD Audio Line input) max in 2 max out 0
# 25 Output () max in 0 max out 2
# 26 Microphone (Steam Streaming Microphone Wave) max in 8 max out 0
# 27 Speakers (Steam Streaming Microphone Wave) max in 0 max out 8
# 28 Input (Steam Streaming Speakers Wave) max in 8 max out 0
# 29 Speakers (Steam Streaming Speakers Wave) max in 0 max out 8