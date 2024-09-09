import numpy as np
from scipy.fft import rfft, irfft
import history


class EqualizerEditor:
    def change_equalizer(self, audio_file, low_freq=None, high_freq=None, gain=None):
        if (low_freq and high_freq and gain) is not None:
            audio_file = self.apply_equalizer(audio_file, low_freq, high_freq, gain)
            return audio_file
        else:
            low_freq, high_freq, gain = self.get_equalizer_params()
            audio_file = self.apply_equalizer(audio_file, low_freq, high_freq, gain)
            return audio_file

    def get_equalizer_params(self):
        while True:
            try:
                print("    Введите параметры эквалайзера:")
                low_freq = float(input("        Нижняя частота (Гц): "))
                high_freq = float(input("        Верхняя частота (Гц): "))
                gain = float(input("        Усиление (в разах): "))

                if low_freq < 0 or high_freq <= low_freq or gain <= 0:
                    print("    Неверные параметры, попробуйте снова.")
                    continue

                return low_freq, high_freq, gain

            except ValueError:
                print("    Пожалуйста, введите корректные числа.")

    def apply_equalizer(self, audio_file, low_freq, high_freq, gain):
        samples = np.array(audio_file.get_array_of_samples())
        sample_rate = audio_file.frame_rate

        fourier = rfft(samples)

        frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)

        valid_freq_mask = (frequencies >= low_freq) & (frequencies <= high_freq)

        fourier[valid_freq_mask] *= gain

        equalized_audio = irfft(fourier)

        equalized_audio = np.int16(equalized_audio / np.max(np.abs(equalized_audio)) * 32767)

        audio_file = audio_file._spawn(equalized_audio.astype(audio_file.array_type))

        audio_file.frame_rate = int(sample_rate)

        history.history_list += f"Эквалайзер применен: Нижняя частота - {low_freq} Гц, " \
                                f"Верхняя частота - {high_freq} Гц, Усиление - {gain} раз\n"
        return audio_file
