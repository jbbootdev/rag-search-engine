from .search_utils import (
    DEFAULT_SEARCH_LIMIT,
    load_movies,
    preprocess_input,
)

from collections import Counter
import math
import pickle
import os

MOVIES = load_movies()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    results = []
    query_tokens = preprocess_input(query)
    index = InvertedIndex()
    index.load()

    for token in query_tokens:
        document_ids = index.get_documents(token)
        for id in document_ids:
            movie = index.docmap[id]
            results.append(movie)
            print(f"{movie['title']} ({movie['id']})")

            if len(results) >= limit:
                return results

    return results


def build_command():
    idx = InvertedIndex()
    idx.build(MOVIES)
    idx.save()


def tf_command(doc_id: int, term: str) -> int:
    idx = InvertedIndex()
    idx.load()
    return idx.get_tf(doc_id, term)


def idf_command(term: str) -> float:
    cleaned_term = preprocess_input(term)
    idx = InvertedIndex()
    idx.load()
    total_doc_count = len(idx.docmap)
    term_match_doc_count = len(idx.index[cleaned_term[0]])
    print("total_doc_count: ", total_doc_count)
    print("term_match_doc_count: ", term_match_doc_count)
    return math.log((total_doc_count + 1) / (term_match_doc_count + 1))


def tfidf_command(doc_id: int, term: str) -> float:
    idx = InvertedIndex()
    idx.load

    tf = tf_command(doc_id, term)
    idf = idf_command(term)

    return tf * idf


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}
        self.term_frequencies = {}

    def __add_document(self, doc_id, text):
        tokens = preprocess_input(text.lower())
        for token in tokens:
            if doc_id not in self.term_frequencies:
                self.term_frequencies[doc_id] = Counter()

            self.term_frequencies[doc_id][token] += 1
            if token not in self.index:
                self.index[token] = set()

            self.index[token].add(doc_id)

    def get_documents(self, term):
        key = term
        if key in self.index:
            list_of_numbers = list(self.index[key])
            sorted_numbers = sorted(list_of_numbers)
            return sorted_numbers

        return []

    def get_tf(self, doc_id, term):
        tokenized_term = preprocess_input(term.lower())

        if len(tokenized_term) == 0:
            return 0

        if len(tokenized_term) > 1:
            raise Exception("Invalid term")

        results = self.term_frequencies.get(doc_id, Counter())
        return results.get(tokenized_term[0], 0)

    def build(self, movies):
        for m in movies:
            id = m["id"]
            text = f"{m['title']} {m['description']}"

            self.docmap[id] = m
            self.__add_document(id, text)

    def load(self):
        file_path = os.path.join(CACHE_PATH, "index.pkl")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                self.index = pickle.load(f)
        else:
            raise FileNotFoundError

        docmap_file_path = os.path.join(CACHE_PATH, "docmap.pkl")
        if os.path.exists(docmap_file_path):
            with open(docmap_file_path, "rb") as docmap_file:
                self.docmap = pickle.load(docmap_file)
        else:
            raise FileNotFoundError

        term_frequency_file_path = os.path.join(CACHE_PATH, "term_frequencies.pkl")
        if os.path.exists(term_frequency_file_path):
            with open(term_frequency_file_path, "rb") as term_frequencies_file:
                self.term_frequencies = pickle.load(term_frequencies_file)
        else:
            raise FileNotFoundError

    def save(self):
        if not os.path.isdir(CACHE_PATH):
            os.makedirs(CACHE_PATH)

        with open(os.path.join(CACHE_PATH, "index.pkl"), "wb") as index_file:
            pickle.dump(self.index, index_file)

        with open(os.path.join(CACHE_PATH, "docmap.pkl"), "wb") as docmap_file:
            pickle.dump(self.docmap, docmap_file)

        with open(
            os.path.join(CACHE_PATH, "term_frequencies.pkl"), "wb"
        ) as term_frequencies_file:
            pickle.dump(self.term_frequencies, term_frequencies_file)
