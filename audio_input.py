import wave
from os import system, remove
from threading import Timer
from pyaudio import PyAudio, paDirectSound, paInt16, paContinue

audio = PyAudio()
chunk_number = 0

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
    default_device = next(
        (index, name) for (index, name) in device_list 
            if name.rfind("Microphone Array") != -1 or name.rfind("FIFINE K690") != -1
    )

    return default_device

def get_recorded_file_name(chunk_number: int = 0):
    import datetime

    now = datetime.datetime.now()

    return f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}_{chunk_number}"

def process_chunk():
    global stream, wave_file, chunk_number, timer, selected_index, current_file_name

    chunk_number += 1
    stream.stop_stream()
    stream.close()
    wave_file.close()

    system(f"encodec --hq recorded/{current_file_name}.wav compressed/{current_file_name}.ecdc")
    remove(f"recorded/{current_file_name}.wav")

    start_record_audio(selected_index, get_recorded_file_name(chunk_number))

def stop_record_audio():
    global stream, wave_file, chunk_number, timer, current_file_name

    wave_file_path = wave_file.getcompname()

    chunk_number = 0
    timer.cancel()
    stream.stop_stream()
    stream.close()
    wave_file.close()

    system(f"encodec --hq recorded/{current_file_name}.wav compressed/{current_file_name}.ecdc")
    remove(f"recorded/{current_file_name}.wav")

def start_record_audio(device_index: int, file_name: str = get_recorded_file_name()):
    global stream, wave_file, chunk_number, timer, selected_index, current_file_name
    selected_index = device_index
    current_file_name = file_name

    FORMAT = paInt16
    CHANNELS = 2
    RATE = 48000
    CHUNK = 1024

    wave_file = wave.open(f"recorded/{file_name}.wav", "wb")
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)

    def stream_callback(in_data, frame_count, time_info, status):
        wave_file.writeframes(in_data)
        return (in_data, paContinue)

    stream = audio.open(
        rate = RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device_index,
        stream_callback=stream_callback
    )

    timer = Timer(600, process_chunk)
    timer.start()

if __name__ == '__main__':
    device_list = get_audio_device_list()
    print(device_list)

    default_device = get_default_audio_device()
    print(default_device)
