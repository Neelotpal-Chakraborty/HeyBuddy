class JokesDB:
    jokes = [
        "Why do Java developers wear glasses? Because they don’t C#.",
        "Debugging: removing the needles from the haystack.",
        "There are only 10 types of people: those who understand binary and those who don’t."
    ]

    @staticmethod
    def get_all_jokes():
        return JokesDB.jokes
