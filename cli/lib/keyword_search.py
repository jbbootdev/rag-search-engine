from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
import string


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    cleaned_query = remove_punctuation_translate(query.lower())
    query_tokens = tokenize(cleaned_query)

    for movie in movies:
        movie_matched = False
        cleaned_movie_title = remove_punctuation_translate(movie["title"].lower())
        movie_tokens = tokenize(cleaned_movie_title)

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


def remove_punctuation_translate(text: str) -> str:
    translator = str.maketrans("", "", string.punctuation)

    return text.translate(translator)


def tokenize(text: str) -> list[str]:
    tokens = text.split()
    non_empty_tokens = [token for token in tokens if token]

    return list(set(non_empty_tokens))
