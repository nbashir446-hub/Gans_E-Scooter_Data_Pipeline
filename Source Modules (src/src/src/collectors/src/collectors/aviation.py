import requests
import pandas as pd
from config.settings import RAPIDAPI_HEADERS

def get_airports(cities_df: pd.DataFrame) -> pd.DataFrame:
    all_airports = []
    url = "https://aerodatabox.p.rapidapi.com/airports/search/location"

    for _, row in cities_df.iterrows():
        querystring = {
            "lat": row["latitude"],
            "lon": row["longitude"],
            "radiusKm": "50",
            "limit": "10",
            "withFlightInfoOnly": "true"
        }
        response = requests.get(url, headers=RAPIDAPI_HEADERS, params=querystring)

        if response.status_code == 200:
            data = response.json()
            airports = pd.json_normalize(data.get('items', []))
            airports["city_id"] = row["city_id"]
            all_airports.append(airports)
        else:
            print(f"WARNING: Failed to retrieve airports for {row['name']}")

    airports_df = pd.concat(all_airports, ignore_index=True)
    return airports_df[["icao", "name", "city_id"]]

def get_flights(airports_df: pd.DataFrame) -> pd.DataFrame:
    arrivals = []
    tomorrow = pd.Timestamp.now().date() + pd.Timedelta(1, "day")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    times = [["00:00", "11:59"], ["12:00", "23:59"]]

    for _, row in airports_df.iterrows():
        for start_time, end_time in times:
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{row['icao']}/{tomorrow_str}T{start_time}/{tomorrow_str}T{end_time}"
            querystring = {
                "withLeg": "false",
                "direction": "Arrival",
                "withCancelled": "false",
                "withCodeshared": "false"
            }
            response = requests.get(url, headers=RAPIDAPI_HEADERS, params=querystring)

            if response.status_code == 200:
                data = response.json().get("arrivals", [])
                for arrival in data:
                    arrival_dict = {
                        "arrive_icao": row["icao"],
                        "depart_icao": arrival["movement"]["airport"].get("icao", None),
                        "depart_airport": arrival["movement"]["airport"].get("name", None),
                        "depart_country": arrival["movement"]["airport"].get("countryCode", None),
                        "arrive_time_scheduled": arrival["movement"]["scheduledTime"].get("local"),
                        "arrive_time_revised": arrival["movement"].get("revisedTime", {}).get("local", None),
                        "flight_number": arrival.get("number", None),
                        "aircraft": arrival.get("aircraft", {}).get("model", None)
                    }
                    arrivals.append(arrival_dict)
            else:
                print(f"WARNING: Failed to retrieve flights for {row['name']}")

    flights_df = pd.DataFrame(arrivals)
    
    if not flights_df.empty:
        flights_df["depart_country"] = flights_df["depart_country"].str.upper()
        flights_df["arrive_time_scheduled"] = pd.to_datetime(flights_df["arrive_time_scheduled"])
        flights_df["arrive_time_revised"] = pd.to_datetime(flights_df["arrive_time_revised"])

    return flights_df
