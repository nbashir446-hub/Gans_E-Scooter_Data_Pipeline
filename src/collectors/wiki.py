import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from config.settings import WIKI_HEADERS


def get_cities_info(cities: list) -> pd.DataFrame:
    """Scrapes country, latitude, and longitude for each city from Wikipedia."""
    records = []

    for city in cities:
        url = f"https://en.wikipedia.org/wiki/{city}"
        response = requests.get(url, headers=WIKI_HEADERS)

        if response.status_code != 200:
            print(f"WARNING: Could not retrieve HTML for {city}")
            continue

        try:
            city_soup = BeautifulSoup(response.content, "html.parser")
            table = city_soup.find("table")

            country = None
            for row in table.find_all("tr"):
                if row.find(string="Country"):
                    country = row.find("a").get_text()
                    break

            lat, lon = table.find(class_="geo").get_text().split("; ")
            try:
                lat, lon = float(lat), float(lon)
            except ValueError:
                lat, lon = None, None

            records.append({
                "city_name": city,
                "country_name": country,
                "latitude": lat,
                "longitude": lon
            })

        except AttributeError as e:
            print(f"WARNING: Could not parse page structure for {city}: {e}")

    return pd.DataFrame(records)


def get_populations(cities_df: pd.DataFrame) -> pd.DataFrame:
    """Scrapes population figures for each city in cities_df from Wikipedia."""
    records = []
    today = date.today()

    for _, city_row in cities_df.iterrows():
        city = city_row["city_name"]
        city_id = city_row["city_id"]
        url = f"https://en.wikipedia.org/wiki/{city}"
        response = requests.get(url, headers=WIKI_HEADERS)

        if response.status_code != 200:
            print(f"WARNING: Could not retrieve HTML for {city}")
            continue

        try:
            city_soup = BeautifulSoup(response.content, "html.parser")
            table = city_soup.find("table")

            population = None
            for tr in table.find_all("tr"):
                if tr.find(string="Population"):
                    population = int(tr.find_next("td").get_text().replace(",", ""))
                    break

            if population is not None:
                records.append({
                    "city_id": city_id,
                    "population": population,
                    "date_gathered": today
                })
            else:
                print(f"WARNING: No population found for {city}")

        except AttributeError as e:
            print(f"WARNING: Could not parse page structure for {city}: {e}")

    return pd.DataFrame(records)
