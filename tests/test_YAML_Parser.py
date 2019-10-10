import unittest
import os
import yaml

from pypublish import YAML

class TestYamlParser(unittest.TestCase):

    def test_file_not_found(self):
        try:
            parser = YAML.Parser()
            parser.load("inexistant.yaml")
            self.fail("Exception not raised")
        except FileNotFoundError:
            pass

    def test_simple_yaml(self):
        expected = {
            "episode": "008",
            "title": "Awakening",
            "author": "Dave & Yannick",
            "podcast": "Tea, Earl Grey, Hot !"
        }
        my_path = os.path.abspath(os.path.dirname(__file__))
        parser = YAML.Parser()
        actual = parser.load(f"{my_path}/assets/simple.yaml")
        self.assertEqual(expected, actual)

    def test_simple_replace(self):
        expected = {
            "episode": "008",
            "title": "Awakening",
            "author": "Dave & Yannick",
            "podcast": "Tea, Earl Grey, Hot !",
            "inputfiles": [
                {"file": "008_music.flac", "type": "music"},
                {"file": "008_yannick.flac"},
                {"file": "008_dave.flac"},
                {"file": "008_guess.flac"},
            ]
        }
        my_path = os.path.abspath(os.path.dirname(__file__))
        parser = YAML.Parser()
        actual = parser.load(f"{my_path}/assets/tokens.yaml")
        self.assertEqual(expected, actual)

    def test_include_empty_file(self):
        expected = {
            "title": "Awakening"
        }
        my_path = os.path.abspath(os.path.dirname(__file__))
        parser = YAML.Parser()
        actual = parser.load(f"{my_path}/assets/include_empty_main.yaml")
        self.assertEqual(expected, actual)

    def test_simple_include(self):
        expected = {
            "episode": "008",
            "title": "Awakening",
            "author": "Dave & Yannick",
            "podcast": "Tea, Earl Grey, Hot !",
            "inputfiles": [
                {"file": "music.flac", "type": "music"},
                {"file": "yannick.flac"},
                {"file": "dave.flac"},
                {"file": "guess.flac"},
            ]
        }
        my_path = os.path.abspath(os.path.dirname(__file__))
        parser = YAML.Parser()
        actual = parser.load(f"{my_path}/assets/simple_main.yaml")
        self.assertEqual(expected, actual)
    
    def test_replace_include(self):
        expected = {
            "episode": "008",
            "title": "Awakening",
            "author": "Dave & Yannick",
            "podcast": "Tea, Earl Grey, Hot !",
            "inputfiles": [
                {"file": "008_music.flac", "type": "music"},
                {"file": "008_yannick.flac"},
                {"file": "008_dave.flac"},
                {"file": "008_guess.flac"},
            ]
        }
        my_path = os.path.abspath(os.path.dirname(__file__))
        parser = YAML.Parser()
        actual = parser.load(f"{my_path}/assets/tokens_main.yaml")
        self.assertEqual(expected, actual)

    def test_reference(self):
        expected = {
            "episode": "008",
            "title": "Awakening",
            "inputfiles": [
                {"file": "008_music.flac", "type": "music"},
                {"file": "008_yannick.flac"},
                {"file": "008_dave.flac"},
                {"file": "008_guess.flac"},
            ],
            "pipeline": [
                {
                    "module": "auphonic",
                    "inputs": [
                        {"file": "008_music.flac", "type": "music"},
                        {"file": "008_yannick.flac"},
                        {"file": "008_dave.flac"},
                        {"file": "008_guess.flac"},
                    ]
                }
            ]
        }
        my_path = os.path.abspath(os.path.dirname(__file__))
        parser = YAML.Parser()
        actual = parser.load(f"{my_path}/assets/reference_main.yaml")
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
