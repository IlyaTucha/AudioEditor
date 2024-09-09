import os
from help_message import display_help_message
import options


class AudioFile:
    def get_audio_file(self):
        valid_formats = ["mp3", "wav", "ogg", "flv"]
        while True:
            try:
                f_name = input("Введите название файла (пример: music.mp3): ")
                extension = f_name.split(".")[-1].lower()
                if f_name.lower() in options.get_yes_options():
                    display_help_message()
                else:
                    file_path = os.path.join(os.getcwd(), 'audiofiles', f_name)
                    if not os.path.isfile(file_path):
                        raise ValueError("Файл не найден, введите корректное название")
                    elif extension not in valid_formats:
                        raise ValueError("Формат файла не поддерживается, выберите файл с другим форматом")
                    else:
                        return f_name, extension
            except ValueError as error:
                print(error)

    def ask_yes_no_question(self, question: str) -> bool:
        while True:
            answer = input(question).lower()
            if answer in options.get_yes_options():
                return True
            elif answer in options.get_no_options():
                return False
            elif answer in options.get_help_options():
                display_help_message()
            else:
                print("Пожалуйста, введите 'yes' или 'no'")

    def want_to_cut(self):
        return self.ask_yes_no_question("Хотите ли вы обрезать аудиофайл?"
                                        " (yes / no): ")

    def want_to_change_speed(self):
        return self.ask_yes_no_question("Хотите ли вы изменить скорость "
                                        "воспроизведения аудиофайла?"
                                        " (yes / no): ")

    def want_to_change_volume(self):
        return self.ask_yes_no_question("Хотите ли вы изменить "
                                        "громкость аудиофайла? (yes / no): ")

    def want_to_apply_equalizer(self):
        return self.ask_yes_no_question("Хотите ли вы использовать эквалайзер? (yes / no): ")

    def get_new_file_info(self):
        while True:
            new_name = input("Введите новое название аудиофайла: ").strip()
            if new_name.lower() in options.get_help_options():
                display_help_message()
            elif not new_name:
                print("Пожалуйста, введите непустое название")
            elif any(c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
                     for c in new_name):
                print("Название не должно содержать "
                      "следующих символов: \\ / : * ? \" < > |")
            else:
                new_extent = input("Выберите формат в котором вы хотите "
                                   "сохранить (mp3, wav, ogg, flv): ").lower()
                if new_extent in options.get_help_options():
                    display_help_message()
                while new_extent not in ["mp3", "wav", "ogg", "flv"]:
                    new_extent = input("Неверный формат, выберите один из сп"
                                       "иска (mp3, wav, ogg, flv): ").lower()
                new_file_path = f"{new_name}.{new_extent}"
                current_directory = os.path.join(os.getcwd(), 'audiofiles')
                full_path = os.path.join(current_directory, new_file_path)
                if os.path.exists(full_path):
                    print(f"Файл с названием {new_name} и"
                          f" расширением {new_extent} уже существует в текущей папке")
                else:
                    return new_name, new_extent

    def process_audio_change(self, audio_file, change_function, change_type, history):
        original_audio_file = audio_file

        audio_file = change_function(audio_file)

        cancel_action = input(f"Хотите ли изменить {change_type} заново или отменить? (redo / undo / no): ")

        if cancel_action == 'undo':
            audio_file = original_audio_file
            history.history_list += f'Отменено изменение: {change_type}\n'
        elif cancel_action == 'redo':
            audio_file = original_audio_file
            audio_file = change_function(audio_file)
        elif cancel_action == "no":
            original_audio_file = audio_file

        return audio_file
