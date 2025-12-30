from .search_utils import (
    DEFAULT_SEARCH_LIMIT,
    load_movies,
    preprocess_input,
    remove_punctuation_translate,
    tokenize,
)

import pickle
import os

MOVIES = load_movies()


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    results = []

    query_tokens = preprocess_input(query)

    for movie in MOVIES:
        movie_matched = False
        movie_tokens = preprocess_input(movie["title"])

        for query_token in query_tokens:
            for movie_token in movie_tokens:
                if query_token in movie_token:
                    movie_matched = True
                    break
            if movie_matched:
                break

        if movie_matched:
            results.append(movie)
        if len(results) >= limit:
            break
    return results


def build_command():
    index = InvertedIndex()
    index.build(MOVIES)
    index.save()
    docs = index.get_documents("merida")

    print(f"First document for token 'merida' = {docs[0]}")


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        tokens = remove_punctuation_translate(text.lower())
        tokens = tokenize(tokens)

        for token in tokens:
            if token not in self.index:
                self.index[token] = set()

            self.index[token].add(doc_id)

    def get_documents(self, term):
        normalized_term = remove_punctuation_translate(term.lower())
        if normalized_term in self.index:
            list_of_numbers = list(self.index[normalized_term])
            sorted_numbers = sorted(list_of_numbers)
            return sorted_numbers

        return []

    def build(self, movies):
        for m in movies:
            id = m["id"]
            text = f"{m['title']} {m['description']}"

            self.docmap[id] = m
            self.__add_document(id, text)

    def save(self):
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")

        if not os.path.isdir(CACHE_PATH):
            os.makedirs(CACHE_PATH)

        with open(os.path.join(CACHE_PATH, "index.pkl"), "wb") as index_file:
            pickle.dump(self.index, index_file)

        with open(os.path.join(CACHE_PATH, "docmap.pkl"), "wb") as docmap_file:
            pickle.dump(self.docmap, docmap_file)
