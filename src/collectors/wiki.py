import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from sqlalchemy import create_engine
import sqlalchemy
from config.settings import WIKI_HEADERS

def get_cities_info(cities: list) -> pd.DataFrame:
    countries, latitudes, longitudes = [], [], []
    for city in cities:
        url = f"https://en.wikipedia.org/wiki/{city}"
        response = requests.get(url, headers=WIKI_HEADERS)
        if response.status_code == 200:
            city_soup = BeautifulSoup(response.content, 'html.parser')
            for row in city_soup.find("table").find_all("tr"):
                if row.find(string="Country"):
                    countries.append(row.find("a").get_text())
            lat, lon = city_soup.find("table").find(class_="geo").get_text().split("; ")
            try:
                latitudes.append(float(lat))
                longitudes.append(float(lon))
            except ValueError:
                latitudes.append(None)
                longitudes.append(None)
        else:
            print(f"WARNING: Could not retrieve HTML for {city}")
            
    cities_df = pd.DataFrame({"name": cities, "country": countries, "latitude": latitudes, "longitude": longitudes})
    
    return cities_df
    
    
def get_populations(cities_df: pd.DataFrame) -> pd.DataFrame:
    populations, city_ids = [], []
    for i, row in cities_df.iterrows():
        city = row["name"]
        city_id = row["city_id"]
        url = f"https://en.wikipedia.org/wiki/{city}"
        response = requests.get(url, headers=WIKI_HEADERS)
        if response.status_code == 200:
            city_soup = BeautifulSoup(response.content, 'html.parser')
            for row in city_soup.find("table").find_all("tr"):
                if row.find(string="Population"):
                    population = int(row.find_next("td").get_text().replace(",", ""))
                    populations.append(population)
                    city_ids.append(city_id)
     pops_df = pd.DataFrame({"city_id": city_ids, "population": populations, "date_gathered": pd.Timestamp.now().date()})
    
    return pops_df
