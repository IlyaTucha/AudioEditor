import os
from pydub import AudioSegment, effects
from cut_editor import CutEditor
from help_message import display_help_message
from speed_editor import SpeedEditor
from volume_editor import VolumeEditor
from equalizer_editor import EqualizerEditor
from audio_file import AudioFile
import options
import history
import tempfile
from pydub.playback import play


def main():
    file = AudioFile()
    volume = VolumeEditor()
    speed = SpeedEditor()
    cut = CutEditor()
    equalizer = EqualizerEditor()

    input_directory = os.path.join(os.getcwd(), 'audiofiles')
    output_directory = input_directory

    filename, extension = file.get_audio_file()
    original_audio_file = AudioSegment.from_file(os.path.join(input_directory, filename), format=extension)
    audio_file = original_audio_file

    answer = input("Если вы хотите узнать, "
                   "что умеет программа, напишите help, -h, --help: ")
    if answer.lower() in options.get_help_options():
        display_help_message()

    if file.want_to_change_volume():
        audio_file = file.process_audio_change(audio_file, volume.change_volume, "громкость", history)

    if file.want_to_change_speed():
        audio_file = file.process_audio_change(audio_file, speed.change_speed, "скорость", history)

    if file.want_to_cut():
        audio_file = file.process_audio_change(audio_file, cut.cut_audio, "обрезка", history)

    if file.want_to_apply_equalizer():
        audio_file = file.process_audio_change(audio_file, equalizer.change_equalizer, "эквалайзер", history)

    new_audio_file = effects.normalize(audio_file)

    print("\nИзменения успешно применены!")
    preview_choice = input("Хотите ли вы предпрослушать измененный"
                           " аудиофайл? (yes / no): ").lower()

    if preview_choice in options.get_yes_options():
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}')
        temp_file_path = temp_file.name
        temp_file.close()
        new_audio_file.export(temp_file_path, format=extension)

        print("Предпрослушивание измененного аудиофайла... (первые 20 секунд)")
        play(new_audio_file[0:20000])
        os.remove(temp_file_path)

    print("Список ваших изменений:\n")
    if history.history_list == "":
        print("Изменений нет.\n")
    else:
        print(history.history_list)
        new_name, new_extension = file.get_new_file_info()
        output_file_path = os.path.join(output_directory, f'{new_name}.{new_extension}')
        new_audio_file.export(output_file_path, format=new_extension)
        print(f"Измененный аудиофайл сохранен: {output_file_path}")
    input()


if __name__ == '__main__':
    main()
