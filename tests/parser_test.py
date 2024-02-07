import unittest
from wiktionary_parser import WiktionaryParser
from word_meaning import WordMeaning


class TestParser(unittest.TestCase):
    def test_get_wiktionary_definition_present_word(self):
        word = "число"
        definitions = WiktionaryParser.get_wiktionary_definition(word)

        self.assertIsInstance(definitions, list)
        self.assertGreater(len(definitions), 0)

        for definition in definitions:
            self.assertIsInstance(definition, WordMeaning)
            self.assertEqual(definition.word, word)

    def test_get_wiktionary_definition_not_present_word(self):
        word = "боитпс"
        definitions = WiktionaryParser.get_wiktionary_definition(word)

        self.assertIsNone(definitions)

    def test_normalized_word(self):
        self.assertEqual(WiktionaryParser._normalized_word("Кодить"), "кодить")
        self.assertEqual(WiktionaryParser._normalized_word("Программирование"), "программирование")
        self.assertEqual(WiktionaryParser._normalized_word("12345"), "")
        self.assertEqual(WiktionaryParser._normalized_word("!@#$%"), "")
