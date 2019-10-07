import unittest
import os

from pypublish.Util.YAMLUtil import YAMLUtil

class TestYamlUtil(unittest.TestCase):

    def test_file_not_found(self):
        try:
            YAMLUtil.load("inexistant.yaml")
            self.fail("Exception not raised")
        except FileNotFoundError:
            pass

    def test_simple_yaml(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        actual = YAMLUtil.load(f"{my_path}/assets/simple.yaml")
        expected = {
            'episode': '008', 
            'title': 'Awakening', 
            'inputfiles': [
                {'file': '{{episode}}_music.flac', 'type': 'music'}, 
                {'file': '{{episode}}_yannick.flac'}, 
                {'file': '{{episode}}_dave.flac'}, 
                {'file': '{{episode}}_guess.flac'}
            ], 
            'author': 'Dave & Yannick', 
            'podcast': 'Tea, Earl Grey, Hot !', 
            'publisher': 'The Other Side Podcast Network', 
            'url': 'https://teaearlgreyhot.org', 
            'license': 'CC-BY-SA', 
            'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/', 
            'year': 'auto', 
            'pipeline': [
                {
                    'module': 'auphonic', 
                    'inputs': [
                        {'file': '{{episode}}_music.flac', 'type': 'music'}, 
                        {'file': '{{episode}}_yannick.flac'}, 
                        {'file': '{{episode}}_dave.flac'}, 
                        {'file': '{{episode}}_guess.flac'}
                    ], 
                    'outputs': [
                        {'basename': 'tea_earl_grey_hot_{{episode}}'}, 
                        {'files': [
                            {'format': 'mp3', 'bitrate': 96, 'mono': True}, 
                            {'format': 'vorbis', 'bitrate': 96, 'mono': True}, 
                            {'format': 'flac', 'mono': True}, 
                            {'format': 'audiogram', 'mono': True}
                        ]}, 
                        {'algorithms': [
                            {'loudnesstarget': -16}, 
                            {'leveler': True}, 
                            {'gate': True}, 
                            {'crossgate': False}
                        ]}
                    ]
                }
            ]
        }
        self.assertEqual(expected, actual)

    def test_simple_replace(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        actual = YAMLUtil.load(f"{my_path}/assets/simple.yaml")
        actual = YAMLUtil.replace_tokens(actual)
        expected = {
            'episode': '008', 
            'title': 'Awakening', 
            'inputfiles': [
                {'file': '008_music.flac', 'type': 'music'}, 
                {'file': '008_yannick.flac'}, 
                {'file': '008_dave.flac'}, 
                {'file': '008_guess.flac'}
            ], 
            'author': 'Dave & Yannick', 
            'podcast': 'Tea, Earl Grey, Hot !', 
            'publisher': 'The Other Side Podcast Network', 
            'url': 'https://teaearlgreyhot.org', 
            'license': 'CC-BY-SA', 
            'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/', 
            'year': 'auto', 
            'pipeline': [
                {
                    'module': 'auphonic', 
                    'inputs': [
                        {'file': '008_music.flac', 'type': 'music'}, 
                        {'file': '008_yannick.flac'}, 
                        {'file': '008_dave.flac'}, 
                        {'file': '008_guess.flac'}
                    ], 
                    'outputs': [
                        {'basename': 'tea_earl_grey_hot_008'}, 
                        {'files': [
                            {'format': 'mp3', 'bitrate': 96, 'mono': True}, 
                            {'format': 'vorbis', 'bitrate': 96, 'mono': True}, 
                            {'format': 'flac', 'mono': True}, 
                            {'format': 'audiogram', 'mono': True}
                        ]}, 
                        {'algorithms': [
                            {'loudnesstarget': -16}, 
                            {'leveler': True}, 
                            {'gate': True}, 
                            {'crossgate': False}
                        ]}
                    ]
                }
            ]
        }
        self.assertEqual(expected, actual)

    def test_include(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        YAMLUtil.load(f"{my_path}/assets/main.yaml")
    
if __name__ == '__main__':
    unittest.main()
