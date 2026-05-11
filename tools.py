import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_BASE_URL = "http://www.omdbapi.com/"


def request_omdb(params: dict) -> dict:
    """
    Внутренняя функция для запроса к OMDb API.
    """
    if not OMDB_API_KEY:
        return {
            "Response": "False",
            "Error": "OMDB_API_KEY не найден. Проверь файл .env"
        }

    try:
        response = requests.get(
            OMDB_BASE_URL,
            params={**params, "apikey": OMDB_API_KEY},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        return {
            "Response": "False",
            "Error": f"Ошибка запроса к OMDb API: {error}"
        }


@tool
def search_movie_by_title(title: str) -> str:
    """
    Ищет фильм по точному названию и возвращает основную информацию:
    название, год, жанр, режиссёр, актёры, рейтинг IMDB, награды и краткий сюжет.

    Args:
        title: Название фильма. Например: Inception, The Matrix, Interstellar.

    Returns:
        Текстовое описание фильма.
    """
    data = request_omdb({"t": title, "plot": "short"})

    if data.get("Response") == "False":
        return f"Фильм '{title}' не найден. Причина: {data.get('Error', 'неизвестная ошибка')}"

    return (
        f"Название: {data.get('Title')}\n"
        f"Год: {data.get('Year')}\n"
        f"Жанр: {data.get('Genre')}\n"
        f"Режиссёр: {data.get('Director')}\n"
        f"Актёры: {data.get('Actors')}\n"
        f"IMDB рейтинг: {data.get('imdbRating')}\n"
        f"Награды: {data.get('Awards')}\n"
        f"Сюжет: {data.get('Plot')}"
    )


@tool
def search_movies_list(query: str) -> str:
    """
    Ищет список фильмов по ключевому слову и возвращает до 5 результатов.

    Args:
        query: Поисковое слово. Например: Batman, Spider Man, Harry Potter.

    Returns:
        Список найденных фильмов с названием, годом и типом.
    """
    data = request_omdb({"s": query})

    if data.get("Response") == "False":
        return f"По запросу '{query}' ничего не найдено. Причина: {data.get('Error', 'неизвестная ошибка')}"

    movies = data.get("Search", [])[:5]

    result = [f"Найденные фильмы по запросу '{query}':"]

    for index, movie in enumerate(movies, start=1):
        result.append(
            f"{index}. {movie.get('Title')} "
            f"({movie.get('Year')}) — тип: {movie.get('Type')}"
        )

    return "\n".join(result)


@tool
def get_full_movie_plot(title: str) -> str:
    """
    Получает полный сюжет фильма по названию.

    Args:
        title: Название фильма. Например: Inception.

    Returns:
        Полный сюжет фильма.
    """
    data = request_omdb({"t": title, "plot": "full"})

    if data.get("Response") == "False":
        return f"Не удалось получить сюжет фильма '{title}'. Причина: {data.get('Error', 'неизвестная ошибка')}"

    return (
        f"Фильм: {data.get('Title')} ({data.get('Year')})\n"
        f"Полный сюжет:\n{data.get('Plot')}"
    )


@tool
def get_movie_rating(title: str) -> str:
    """
    Получает рейтинг IMDB фильма по названию.

    Args:
        title: Название фильма. Например: Inception.

    Returns:
        Рейтинг IMDB и базовая информация о фильме.
    """
    data = request_omdb({"t": title})

    if data.get("Response") == "False":
        return f"Не удалось получить рейтинг фильма '{title}'. Причина: {data.get('Error', 'неизвестная ошибка')}"

    return (
        f"Фильм: {data.get('Title')} ({data.get('Year')})\n"
        f"IMDB рейтинг: {data.get('imdbRating')}\n"
        f"Жанр: {data.get('Genre')}\n"
        f"Режиссёр: {data.get('Director')}"
    )
