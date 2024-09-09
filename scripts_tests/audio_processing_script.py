import sys

sys.path.append('C:\\Users\\User\\Desktop\\AudioEditor')
import os
from pydub import AudioSegment
from volume_editor import VolumeEditor
from speed_editor import SpeedEditor
from cut_editor import CutEditor
from equalizer_editor import EqualizerEditor


def process_audio_file(input_path):
    audio_file = AudioSegment.from_file(input_path)

    volume = VolumeEditor()  # for changing volume (increase True = up, False = down)
    audio_file = volume.change_volume(audio_file, increase=True, decibels=20)

    speed = SpeedEditor()  # for changing speed
    audio_file = speed.change_speed(audio_file, speed_factor=1.1)

    cut = CutEditor()  # for cutting audio (in sec)
    audio_file = cut.cut_audio(audio_file, start_time=0, end_time=60)

    equalizer = EqualizerEditor()  # for equalizing audio
    audio_file = equalizer.change_equalizer(audio_file, low_freq=10, high_freq=3000, gain=4)

    _, extension = os.path.splitext(input_path)
    output_path = os.path.join(os.getcwd(), f"{os.path.basename(input_path).split('.')[0]}_updated{extension}")
    audio_file.export(output_path, format=extension[1:])

    return output_path


def main():
    valid_extensions = [".mp3", ".wav", ".ogg", ".flv"]

    for filename in os.listdir(os.getcwd()):
        _, extension = os.path.splitext(filename)
        if extension.lower() in valid_extensions:
            input_path = os.path.join(os.getcwd(), filename)
            processed_file = process_audio_file(input_path)
            print(f"Измененный аудиофайл сохранен по пути: {processed_file}")


if __name__ == '__main__':
    main()
    input("Нажмите Enter, чтобы закрыть программу...")
