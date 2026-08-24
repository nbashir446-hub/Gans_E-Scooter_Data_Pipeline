import pandas as pd
from config.settings import CONNECTION_STRING
from src.utils.helpers import enter_cities
from src.collectors.wiki import get_cities_info

def main():
    cities = enter_cities()
    if len(cities) > 0:
        cities_df = get_cities_info(cities)
        cities_df.to_sql("cities", con=CONNECTION_STRING, if_exists="append", index=False)
        print("✅ Cities added successfully!")

if __name__ == "__main__":
    main()
