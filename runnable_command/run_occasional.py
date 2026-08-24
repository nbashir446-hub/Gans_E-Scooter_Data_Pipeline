import pandas as pd
from config.settings import CONNECTION_STRING
from src.collectors.wiki import get_populations
from src.collectors.aviation import get_airports

def main():
    print("⏳ Executing occasional data updates...")
    cities_df = pd.read_sql("cities", con=CONNECTION_STRING)

    pop_df = get_populations(cities_df)
    pop_df.to_sql("populations", con=CONNECTION_STRING, if_exists="append", index=False)

    airports_df = get_airports(cities_df)
    airports_df.to_sql("airports", con=CONNECTION_STRING, if_exists="append", index=False)
    print("✅ Occasional updates completed!")

if __name__ == "__main__":
    main()
