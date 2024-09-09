import history
from help_message import display_help_message
import options as options


class VolumeEditor:
    def change_volume(self, audio_file, increase=None, decibels=None):
        if decibels is not None:
            return self.apply_volume_change(audio_file, decibels, increase)
        else:
            return self.prompt_volume_change(audio_file)

    def apply_volume_change(self, audio_file, decibels, increase=None):
        if increase:
            audio_file = self.increase_volume(audio_file, decibels)
        else:
            audio_file = self.decrease_volume(audio_file, decibels)

        return audio_file

    def prompt_volume_change(self, audio_file):
        while True:
            answer = input("    Вы хотите повысить или понизить громкость?"
                           " (up / down): ").lower()
            if answer in options.get_help_options():
                display_help_message()
            elif answer == "up" or answer == "down":
                return self.process_volume_change(audio_file, answer)
            else:
                print("    Пожалуйста, введите 'up' или 'down'")

    def process_volume_change(self, audio_file, direction):
        while True:
            try:
                action_description = "повысить" if direction == "up" else "понизить"
                db = input(f"        Введите количество децибел, на которое"
                           f" вы хотите {action_description} громкость: ")
                if db in options.get_help_options():
                    display_help_message()
                    continue

                if direction == "up":
                    audio_file = self.increase_volume(audio_file, db)
                else:
                    audio_file = self.decrease_volume(audio_file, db)

                return audio_file
            except ValueError:
                print("        Пожалуйста, введите число")

    def increase_volume(self, audio_file, decibels):
        audio_file = audio_file + float(decibels)
        history.history_list += f"Громкость повышена на {decibels} дБ\n"\
            if float(decibels) != 0 else "Громкость не изменена\n"
        return audio_file

    def decrease_volume(self, audio_file, decibels):
        audio_file = audio_file - float(decibels)
        history.history_list += f"Громкость понижена на {decibels} дБ\n"\
            if float(decibels) != 0 else "Громкость не изменена\n"
        return audio_file
