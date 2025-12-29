from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords
import string

MOVIES = load_movies()
STOPWORDS = load_stopwords()


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


def preprocess_input(input: str) -> list[str]:
    results = remove_punctuation_translate(input.lower())
    results = tokenize(results)
    results = remove_stopwards(results)
    return results


def remove_stopwards(input: list[str]) -> list[str]:
    return list(set(input) - set(STOPWORDS))


def remove_punctuation_translate(text: str) -> str:
    translator = str.maketrans("", "", string.punctuation)

    return text.translate(translator)


def tokenize(text: str) -> list[str]:
    tokens = text.split()
    non_empty_tokens = [token for token in tokens if token]

    return list(set(non_empty_tokens))
