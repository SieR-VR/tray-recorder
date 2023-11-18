from pystray import Icon, Menu, MenuItem
from audio_input import get_audio_device_list, get_default_audio_device, start_record_audio, stop_record_audio

from PIL import Image, ImageDraw

audio_device_list = get_audio_device_list()
default_device = get_default_audio_device(audio_device_list)

print(audio_device_list)

selected_index = default_device[0]
selected_device = default_device[1]

def refresh_audio_device_list():
    global selected_index, selected_device, audio_device_list, default_device

    audio_device_list = get_audio_device_list()
    default_device = get_default_audio_device(audio_device_list)

    selected_index, selected_device = default_device
    icon.update_menu()

def set_audio_device(index, device_name):
    _index = index
    _device_name = device_name

    def _set_audio_device():    
        print(_index, _device_name)
        global selected_index, selected_device

        selected_index = _index
        selected_device = _device_name
        print(selected_device, _device_name)
        icon.update_menu()

    return _set_audio_device

def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

is_recording = False
toggle_text = "Start Recording"



def toggle_recording():
    global is_recording, selected_index, toggle_text

    is_recording = not is_recording
    toggle_text = "Stop Recording" if is_recording else "Start Recording"

    if is_recording:
        start_record_audio(selected_index)
    else:
        stop_record_audio()

icon = Icon(
    'tray-recorder', 
    icon=create_image(64, 64, 'black', 'white'),
    menu=Menu(
        MenuItem(lambda text: toggle_text, toggle_recording),
        MenuItem('Devices', Menu(
            lambda: [MenuItem(device_name, set_audio_device(index, device_name)) for (index, device_name) in audio_device_list] +
            [MenuItem("Refresh", refresh_audio_device_list)]
        )),
        MenuItem(lambda text: ("Selected: " + selected_device), lambda: (), enabled=False),
        MenuItem('Exit', lambda: icon.stop())
    )
)

icon.run()

