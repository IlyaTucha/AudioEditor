import history
from help_message import display_help_message
import options


class SpeedEditor:
    def change_speed(self, audio, speed_factor=None):
        if speed_factor is not None:
            return self.apply_speed(audio, float(speed_factor))
        else:
            return self.prompt_speed_input(audio)

    def apply_speed(self, audio, speed):
        history_message = self.get_history_message(speed)
        updated_sound = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * float(speed))
        })
        return updated_sound.set_frame_rate(audio.frame_rate)

    def prompt_speed_input(self, audio):
        while True:
            speed_str = input("    Введите скорость воспроизведения аудиофайла"
                              " (пример: 1.5 для ускорения"
                              " или 0.75 для замедления): ")
            if speed_str.lower() in options.get_help_options():
                display_help_message()
                continue
            try:
                speed = float(speed_str)
                if speed == 0:
                    print("    Пожалуйста, введите корректное число")
                    continue
                return self.apply_speed(audio, speed)
            except ValueError:
                print("    Пожалуйста, введите число")

    def get_history_message(self, speed):
        if speed > 1:
            message = f"Скорость воспроизведения увеличена в х{speed} раза\n"
        elif speed < 1:
            message = f"Скорость воспроизведения уменьшена в х{speed} раза\n"
        else:
            message = "Скорость воспроизведения не изменена\n"

        history.history_list += message

        return message
