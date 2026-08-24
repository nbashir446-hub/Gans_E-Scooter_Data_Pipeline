import requests
import pandas as pd
from config.settings import OPENWEATHER_KEY

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

    return pd.DataFrame(forecasts)
