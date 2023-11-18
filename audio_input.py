import wave
from pyaudio import PyAudio, paDirectSound, paInt16

audio = PyAudio()

def get_audio_device_list() -> list[tuple[int, str]]:
    host_api_info = audio.get_host_api_info_by_type(paDirectSound)
    
    host_api_index = host_api_info["index"]
    device_count = audio.get_device_count()

    device_list: list = []
    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)

        if device_info["hostApi"] == host_api_index and device_info["maxInputChannels"] != 0:
            device_list.append(device_info)

    return [(device["index"], device["name"]) for device in device_list]

def get_default_audio_device(device_list: list[tuple[int, str]] = get_audio_device_list()):
    default_device = next((index, name) for (index, name) in device_list if name.rfind("Microphone Array") != -1)

    return default_device

def start_record_audio(device_index: int):
    global stream, wave_file

    wave_file = wave.open("output.wav", "wb")

    def stream_callback(in_data, frame_count, time_info, status):
        
    
    FORMAT = paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024

    stream = audio.open(
        rate = RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device_index,
        stream_callback=stream_callback
    )

if __name__ == '__main__':
    device_list = get_audio_device_list()
    print(device_list)

    default_device = get_default_audio_device()
    print(default_device)
