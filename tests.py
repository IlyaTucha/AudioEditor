import os
import unittest
from pydub import AudioSegment
from unittest.mock import patch
from io import StringIO
import history
from audio_file import AudioFile
from cut_editor import CutEditor
from speed_editor import SpeedEditor
from volume_editor import VolumeEditor


class TestVolumeEditor(unittest.TestCase):
    def setUp(self):
        self.volume_editor = VolumeEditor()
        self.audio_file = AudioFile()

    def test_want_to_change_volume_yes(self):
        with patch('builtins.input', return_value='yes'):
            self.assertTrue(self.audio_file.want_to_change_volume())

    def test_want_to_change_volume_no(self):
        with patch('builtins.input', return_value='no'):
            self.assertFalse(self.audio_file.want_to_change_volume())

    def test_want_to_change_volume_invalid_input(self):
        with patch('builtins.input', side_effect=['invalid', 'no']):
            self.assertFalse(self.audio_file.want_to_change_volume())

    def test_change_volume_up(self):
        with patch('builtins.input', side_effect=['up', '6']):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            new_audio_file = self.volume_editor.change_volume(audio_file)
            self.assertEqual(len(new_audio_file), len(audio_file))

    def test_change_volume_down(self):
        with patch('builtins.input', side_effect=['down', '6']):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            new_audio_file = self.volume_editor.change_volume(audio_file)
            self.assertEqual(len(new_audio_file), len(audio_file))
            self.assertIn("Громкость понижена на 6 дБ", history.history_list.strip())

    def test_change_volume_zero_db(self):
        with patch('builtins.input', side_effect=['down', '0']):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            new_audio_file = self.volume_editor.change_volume(audio_file)
            self.assertEqual(len(new_audio_file), len(audio_file))
            self.assertEqual(new_audio_file.rms, audio_file.rms)
            self.assertIn("Громкость не изменена", history.history_list.strip())

    def test_change_volume_invalid_db_input(self):
        with patch('builtins.input', side_effect=['up', 'invalid', '6']):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            new_audio_file = self.volume_editor.change_volume(audio_file)
            self.assertEqual(len(new_audio_file), len(audio_file))


class TestSpeedEditor(unittest.TestCase):
    def setUp(self):
        self.speed_editor = SpeedEditor()
        self.audio_file = AudioFile()

    def test_want_to_change_speed_yes(self):
        with patch('builtins.input', return_value='yes'):
            self.assertTrue(self.audio_file.want_to_change_speed())

    def test_want_to_change_speed_no(self):
        with patch('builtins.input', return_value='no'):
            self.assertFalse(self.audio_file.want_to_change_speed())

    def test_want_to_change_speed_help(self):
        with patch('builtins.input', side_effect=['help', 'no']):
            self.assertFalse(self.audio_file.want_to_change_speed())

    def test_change_speed_valid_speed_up(self):
        with patch('builtins.input', return_value='2'):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            audio_file.set_frame_rate(44100)
            new_audio_file = self.speed_editor.change_speed(audio_file)
            self.assertAlmostEqual(len(new_audio_file), len(audio_file) / 2, delta=1000)

    def test_change_speed_valid_speed_down(self):
        with patch('builtins.input', side_effect=['0.5']):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            new_audio_file = self.speed_editor.change_speed(audio_file)
            self.assertEqual(len(new_audio_file) * 0.5, len(audio_file))
            self.assertAlmostEqual(len(audio_file) / len(new_audio_file), 0.5, delta=1)
            self.assertIn("Скорость воспроизведения уменьшена в х0.5", history.history_list)

    def test_change_speed_zero_speed(self):
        audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
        with patch('builtins.input', side_effect=['0']):
            with self.assertRaises(Exception):
                new_audio_file = self.speed_editor.change_speed(audio_file)
                self.assertEqual(len(new_audio_file), len(audio_file))
                self.assertIn("Пожалуйста, введите корректное число",
                              history.history_list)

    def test_change_speed_invalid_speed_input(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('builtins.input', side_effect=['abc', '', '1.5']):
                audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
                new_audio_file = self.speed_editor.change_speed(audio_file)
                self.assertAlmostEqual(len(new_audio_file) * 1.5, len(audio_file), delta=1.0)
                self.assertAlmostEqual(len(audio_file) / len(new_audio_file), 1.5, delta=0.1)
                self.assertIn("Пожалуйста, введите число", fake_output.getvalue())
            self.assertIn("Скорость воспроизведения увеличена в х1.5 раза", history.history_list)


class TestCutEditor(unittest.TestCase):
    def setUp(self):
        self.cut_editor = CutEditor()
        self.audio_file = AudioFile()

    def test_want_to_cut_input_yes(self):
        with patch('builtins.input', return_value='yes'):
            self.assertTrue(self.audio_file.want_to_cut())

    def test_want_to_cut_input_no(self):
        with patch('builtins.input', return_value='no'):
            self.assertFalse(self.audio_file.want_to_cut())

    def test_cut_audio_correct_input(self):
        with patch('builtins.input', side_effect=['help', '10 20']):
            audio_file = AudioSegment.from_file(os.path.join(os.getcwd(), 'audiofiles', 'agata.mp3'), format='mp3')
            new_audio_file = self.cut_editor.cut_audio(audio_file)
            self.assertAlmostEqual(len(new_audio_file), 10000)
            self.assertEqual("Аудиофайл обрезан от 10 до 20 секунды", history.history_list.split('\n')[-2])


class TestAudioFile(unittest.TestCase):
    def setUp(self):
        self.audio_file = AudioFile()

    def test_get_audio_file_valid_input(self):
        with patch('builtins.input', return_value='agata.mp3'):
            filename, extension = self.audio_file.get_audio_file()
            self.assertEqual(filename, 'agata.mp3')
            self.assertEqual(extension, 'mp3')

    def test_get_audio_file_invalid_format(self):
        with patch('builtins.input', side_effect=["agata.mp4",
                                                  "agata.mp3"]):
            result = self.audio_file.get_audio_file()
        self.assertEqual(result, ("agata.mp3", "mp3"))

    def test_get_audio_file_file_not_found(self):
        with patch('builtins.input', side_effect=["notagata.mp3",
                                                  "agata.mp3"]):
            result = self.audio_file.get_audio_file()
        self.assertEqual(result, ("agata.mp3", "mp3"))

    def test_get_new_file_info_valid(self):
        with patch('builtins.input', side_effect=["agata", "wav"]):
            self.assertEqual(("agata", "wav"), self.audio_file.get_new_file_info())

    def test_get_new_file_info_invalid_characters(self):
        with patch('builtins.input', side_effect=["ag*ta", "agata", "wav"]):
            result = self.audio_file.get_new_file_info()
            self.assertEqual(result, ("agata", "wav"))

    def test_get_new_file_info_file_already_exists(self):
        with patch('builtins.input', side_effect=["agata", "mp3", "newagata", "wav"]):
            result = self.audio_file.get_new_file_info()
            self.assertEqual(result, ("newagata", "wav"))


if __name__ == '__main__':
    unittest.main()
