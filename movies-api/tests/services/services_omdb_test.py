import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from movies_api.services.omdb import get_movie_by_title, get_movie_by_id, get_n_movies


def test_get_movie_by_title():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "Title": "The Matrix",
            "Year": "1999",
            "imdbID": "tt0133093",
            "Type": "movie",
        }
        response = get_movie_by_title("api_key", "url", "The Matrix")
        assert response == {
            "Title": "The Matrix",
            "Year": "1999",
            "imdbID": "tt0133093",
            "Type": "movie",
        }


@pytest.mark.asyncio
async def test_get_movie_by_id():
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(
            return_value={
                "Title": "The Matrix",
                "Year": "1999",
                "imdbID": "tt0133093",
                "Type": "movie",
            }
        )
        async with aiohttp.ClientSession() as session:
            response = await get_movie_by_id("api_key", "url", session, "tt0133093")
            assert response == {
                "Title": "The Matrix",
                "Year": "1999",
                "imdbID": "tt0133093",
                "Type": "movie",
            }


@pytest.mark.asyncio
async def test_get_n_movies():
    with patch("aiohttp.ClientSession.get") as mock_get:
        with patch("movies_api.services.omdb.get_movie_by_id") as mock_get_movie_by_id:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={
                    "Search": [
                        {"imdbID": "tt0133093"},
                        {"imdbID": "tt0234215"},
                        {"imdbID": "tt0234216"},
                    ]
                }
            )
            mock_get_movie_by_id.side_effect = [
                {
                    "Title": "The Matrix",
                },
                {
                    "Title": "The Matrix Reloaded",
                },
                {
                    "Title": "The Matrix Revolutions",
                },
            ]
            response = await get_n_movies("api_key", "url", 3)
            assert response == [
                {"Title": "The Matrix"},
                {"Title": "The Matrix Reloaded"},
                {"Title": "The Matrix Revolutions"},
            ]


@pytest.mark.asyncio
async def test_get_n_movies_no_search():
    with patch("aiohttp.ClientSession.get") as mock_get:
        with patch("movies_api.services.omdb.get_movie_by_id") as mock_get_movie_by_id:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={
                    "nope": [
                        {"imdbID": "tt0133093"},
                        {"imdbID": "tt0234215"},
                        {"imdbID": "tt0234216"},
                    ]
                }
            )
            mock_get_movie_by_id.side_effect = [
                {
                    "Title": "The Matrix",
                },
                {
                    "Title": "The Matrix Reloaded",
                },
                {
                    "Title": "The Matrix Revolutions",
                },
            ]
            response = await get_n_movies("api_key", "url", 3)
            assert response == []
