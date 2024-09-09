import history
from help_message import display_help_message
import options


class CutEditor:
    def cut_audio(self, audio_file, start_time=None, end_time=None):
        if start_time is not None and end_time is not None:
            audio_file = self.perform_cut(audio_file, start_time, end_time)
            return audio_file
        else:
            return self.process_cut_input(audio_file)

    def process_cut_input(self, audio_file):
        while True:
            try:
                command = input("    Введите диапазон секунд через пробел, "
                                "который вы хотите получить из аудиофайла: ")
                if command.lower() in options.get_help_options():
                    display_help_message()
                    continue

                start_time, end_time = map(int, command.split())
                if start_time < 0 or end_time < 0 or start_time >= end_time \
                        or end_time >= len(audio_file) / 1000:
                    print("    Пожалуйста, введите корректные значения времени")
                else:
                    audio_file = self.perform_cut(audio_file, start_time, end_time)
                    return audio_file

            except ValueError:
                print("    Пожалуйста, введите числа")

    def perform_cut(self, audio_file, start_time, end_time):
        audio_file = audio_file[start_time * 1000:end_time * 1000]
        history.history_list += f"Аудиофайл обрезан от {start_time} до {end_time} секунды\n"
        return audio_file
