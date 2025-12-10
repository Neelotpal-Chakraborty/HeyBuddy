from app.utils.jokes_db import JokesDB
from datetime import date
import httpx

class JokesService:

    @staticmethod
    def get_daily_joke():
        today = date.today().toordinal()
        jokes = JokesDB.get_all_jokes()
        return {
            "date": str(date.today()),
            "joke": jokes[today % len(jokes)]
        }

    @staticmethod
    async def get_random_joke():
        url = "https://official-joke-api.appspot.com/random_joke"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "setup": data.get("setup"),
                    "punchline": data.get("punchline"),
                    "source": "official-joke-api"
                }
            return {"error": "Failed to fetch joke from external API."}
