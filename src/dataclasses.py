from dataclasses import dataclass


@dataclass
class Word:
    root_word: str

    diacritized_word: str
    diacritized_word_sensitive: str

    useful_for_flashcard: bool

    cefr_level: str
    english_translation: str
    romanization: str
    pos: str

    example_sentence_native: str
    example_sentence_english: str

    word_frequency: int
