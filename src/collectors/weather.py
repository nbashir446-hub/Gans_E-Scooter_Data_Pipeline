import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from config.settings import RAPIDAPI_HEADERS

def get_forecasts(cities_df: pd.DataFrame) -> pd.DataFrame:
    forecasts = []
    url = "https://api.openweathermap.org/data/2.5/forecast"
    for _, row in cities_df.iterrows():
        params = {
            "lat": row["latitude"],
            "lon": row["longitude"],
            "appid": OPENWEATHER_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        response_json = response.json()
        for forecast in response_json.get('list', []):
            forecast_data = {
                "city": data["city"]["name"],
                        "country": data["city"]["country"],
                        "forecast_time": entry["dt_txt"],
                        "temp_c": entry["main"]["temp"],
                        "feels_like_c": entry["main"]["feels_like"],
                        "humidity_pct": entry["main"]["humidity"],
                        "outlook": entry["weather"][0]["description"],
                        "wind_speed_m_s": entry["wind"]["speed"],
                        "rain_prob": entry["pop"],
            }
            forecasts.append(forecast_data)
    return pd.DataFrame(forecasts)import requests


OR

import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from config.settings import RAPIDAPI_HEADERS

def get_forecasts(cities_df: pd.DataFrame) -> pd.DataFrame:
    forecasts = []
    url = "https://api.openweathermap.org/data/2.5/forecast"

    for _, row in cities_df.iterrows():
        params = {
            "lat": row["latitude"],
            "lon": row["longitude"],
            "appid": OPENWEATHER_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            response_json = response.json()

            for forecast in response_json.get("list", []):
                forecast_data = {
                    "city_id": row["city_id"],
                    "city_name": row["city_name"],
                    "country_name": row["country_name"],
                    "forecast_time": forecast["dt_txt"],
                    "temperature": forecast["main"]["temp"],
                    "feels_like": forecast["main"]["feels_like"],
                    "humidity": forecast["main"]["humidity"],
                    "outlook": forecast["weather"][0]["description"],
                    "wind_speed_m_s": forecast["wind"]["speed"],
                    "rain_prob": forecast["pop"],
                }
                forecasts.append(forecast_data)

        except Exception as e:
            print(f"⚠️ Error fetching weather for city_id {row['city_id']}: {e}")

    forecasts_df = pd.DataFrame(forecasts)

    if not forecasts_df.empty:
        forecasts_df["forecast_time"] = pd.to_datetime(forecasts_df["forecast_time"])

    return forecasts_df
