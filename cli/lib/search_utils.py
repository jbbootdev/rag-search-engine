import json
import os
import string

from nltk.stem import PorterStemmer
from nltk.stem.snowball import stopwords

DEFAULT_SEARCH_LIMIT = 5

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")


def load_movies() -> list[dict]:
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data["movies"]


def load_stopwords() -> list[str]:
    with open(STOPWORDS_PATH, "r") as f:
        words = f.read().splitlines()
    return words


def preprocess_input(inputs: str) -> list[str]:
    results = remove_punctuation_translate(inputs.lower())
    results = tokenize(results)
    results = remove_stopwards(results)
    results = perform_stemming(results)
    return results


def perform_stemming(inputs: list[str]) -> list[str]:
    stemmer = PorterStemmer()
    stemmed_inputs = [stemmer.stem(word) for word in inputs]
    return stemmed_inputs


def remove_stopwards(input: list[str]) -> list[str]:
    stopwords = set(load_stopwords())
    return [word for word in input if word not in stopwords]


def remove_punctuation_translate(text: str) -> str:
    translator = str.maketrans("", "", string.punctuation)

    return text.translate(translator)


def tokenize(text: str) -> list[str]:
    tokens = text.split()
    non_empty_tokens = [token for token in tokens if token]

    return non_empty_tokens
