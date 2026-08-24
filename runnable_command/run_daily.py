import pandas as pd
from config.settings import CONNECTION_STRING
from src.collectors.weather import get_forecasts
from src.collectors.aviation import get_flights

def main():
    print("⏳ Executing daily data updates...")
    cities_df = pd.read_sql("cities", con=CONNECTION_STRING)
    airports_df = pd.read_sql("SELECT * FROM airports WHERE `active` = 1", con=CONNECTION_STRING)

    forecasts_df = get_forecasts(cities_df)
    forecasts_df.to_sql("forecasts", con=CONNECTION_STRING, if_exists="append", index=False)

    flights_df = get_flights(airports_df)
    flights_df.to_sql("flights", con=CONNECTION_STRING, if_exists="append", index=False)
    print("✅ Daily updates completed!")

if __name__ == "__main__":
    main()
