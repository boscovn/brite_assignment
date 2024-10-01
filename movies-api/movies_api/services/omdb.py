import aiohttp
import asyncio
import requests


async def get_movie_by_id(
    api_key, url, session: aiohttp.ClientSession, imdb_id
) -> dict:
    """Get movie details by IMDb ID asynchronously."""
    params = {"apikey": api_key, "i": imdb_id}
    async with session.get(url, params=params) as response:
        # This need some sort of error handling

        return await response.json()


def get_movie_by_title(api_key, url, title) -> dict:
    params = {"apikey": api_key, "t": title}
    response = requests.get(url, params=params)
    return response.json()


async def get_n_movies(api_key, url, num_movies) -> list:
    print("Fetching movies...")
    """Fetch n movies asynchronously."""
    ids = []
    page = 1

    async with aiohttp.ClientSession() as session:
        while len(ids) < num_movies:
            params = {"apikey": api_key, "s": "they", "page": page}
            async with session.get(url, params=params) as response:
                response_json = await response.json()

                if "Search" not in response_json:
                    print(
                        f"Error in fetching movies: {response_json.get('Error', 'Unknown error')}"
                    )
                    break

                ids += [movie["imdbID"] for movie in response_json["Search"]]
                page += 1

        tasks = [
            get_movie_by_id(api_key, url, session, imdb_id)
            for imdb_id in ids[:num_movies]
        ]
        return await asyncio.gather(*tasks)
