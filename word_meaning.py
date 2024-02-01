class WordMeaning(object):
    """
    Class containing definition of a word and examples to definition

    Attributes:
        word: The word itself
        definition: Single definition of the word
        examples: List containing cases of the word usage in the definition
    """
    def __init__(self, word):
        self.word = word
        self.definition = ""
        self.examples = []

    def __repr__(self):
        return f"{self.word}: {self.definition}\n{self.examples}"

    def add_example(self, example):
        self.examples.append(example)

    def is_empty(self):
        return self.definition == ""
