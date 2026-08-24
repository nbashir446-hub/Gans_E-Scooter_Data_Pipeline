import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("CON_STRING")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

WIKI_HEADERS = {'User-Agent': 'Chrome/134.0.0.0'}
RAPIDAPI_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com",
    "Content-Type": "application/json"
}
