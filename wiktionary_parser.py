import bs4.element
import requests
from bs4 import BeautifulSoup, NavigableString
import re
from word_meaning import WordMeaning


class WiktionaryParser:
    """
    Parser of Russian Wiktionary
    https://ru.wiktionary.org/wiki/
    """
    @classmethod
    def get_wiktionary_definition(cls, word) -> list[WordMeaning]:
        """
        Parse Russian Wiktionary and find the word definition with examples

        :param word: Word, definition of which it is needed to find
        :return: One or multiple definitions of the word
        """
        word = cls._normalized_word(word)
        request = f"https://ru.wiktionary.org/wiki/{word}"
        response = requests.get(request)

        if response.status_code == 200:
            found_meanings = []
            html_text = response.text
            soup = BeautifulSoup(html_text, "html.parser")
            meanings = soup.find("span", id="Значение").find_next("ol")

            # Iterate through all the meanings of word
            for meaning in meanings.findChildren("li"):
                current_meaning = WordMeaning(word)

                for element in meaning:
                    # If element is just text (no HTML tags), push it into the definition
                    if isinstance(element, NavigableString):
                        current_meaning.definition += element.text

                    elif isinstance(element, bs4.Tag):
                        if cls._is_example_block(element):
                            # If element is example of the word usage, push it into the examples
                            cls._delete_example_metadata(element)

                            for example in element:
                                if cls._contains_letters(example.text):
                                    current_meaning.add_example(example.text.strip())
                        elif cls._is_text_block(element):
                            current_meaning.definition += element.text

                if not current_meaning.is_empty():
                    found_meanings.append(current_meaning)
            return found_meanings

    @staticmethod
    def _normalized_word(word: str):
        """ Normalize the word bringing it to lower case and deleting all the symbols except Russian letters """
        word = word.lower()
        word = re.sub(r"[^а-яё]", "", word)
        return word

    @staticmethod
    def _is_example_block(element: bs4.Tag):
        return "example-fullblock" in element.get_attribute_list("class")

    @staticmethod
    def _is_text_block(element: bs4.Tag):
        if element.get_attribute_list("class") and WiktionaryParser._contains_letters(element.text):
            return True
        return False

    @staticmethod
    def _contains_letters(text: str) -> bool:
        return re.search(r"[а-я]", text) is not None

    @staticmethod
    def _delete_example_metadata(element: bs4.Tag):
        """ Delete metadata in example section (details and absent) """
        for example_detail in element.findChildren("span", class_="example-details"):
            example_detail.extract()
        for example_absent in element.findChildren("span", class_="example-absent"):
            example_absent.extract()


if __name__ == "__main__":
    definitions = WiktionaryParser.get_wiktionary_definition("кодить")
    if definitions:
        print("\n\n".join([a.__repr__() for a in definitions]))
