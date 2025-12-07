from app.utils.jokes_db import JokesDB
from datetime import date

class JokesService:

    @staticmethod
    def get_daily_joke():
        today = date.today().toordinal()
        jokes = JokesDB.get_all_jokes()
        return {
            "date": str(date.today()),
            "joke": jokes[today % len(jokes)]
        }
