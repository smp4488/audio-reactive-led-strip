import time
import numpy as np
import pyaudio
import config

# import sounddevice
# with sounddevice.OutputStream(device="USB Audio Device", channels=8, callback=callback, samplerate=SAMPLE_RATE):

SAMPLE_RATE = 44100


def start_stream(callback):
    
    
    p = pyaudio.PyAudio()

    # print ( "Available devices:\n")
    for i in range(0, p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print ( str(info["index"]) +  ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
        pass
    
    for i in range(0, p.get_device_count()):
        print(i, p.get_device_info_by_index(i)['name'])
    device_id = 1
    device_info = p.get_device_info_by_index(device_id)
    frames_per_buffer = int(config.MIC_RATE / config.FPS)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.MIC_RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=1,
                    as_loopback=True)
    overflows = 0
    prev_ovf_time = time.time()
    while True:
        try:
            y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            y = y.astype(np.float32)
            stream.read(stream.get_read_available(), exception_on_overflow=False)
            callback(y)
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    p.terminate()
