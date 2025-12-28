from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
import string


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    cleaned_query = remove_punctuation_translate(query.lower())
    for movie in movies:
        if cleaned_query in remove_punctuation_translate(movie["title"].lower()):
            results.append(movie)
            if len(results) >= limit:
                break
    return results


def remove_punctuation_translate(text: str) -> str:
    translator = str.maketrans("", "", string.punctuation)

    return text.translate(translator)
