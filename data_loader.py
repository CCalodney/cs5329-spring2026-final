import csv
import os
import sys
import urllib.request
from geopy.distance import geodesic


AIRPORTS_FILE = "data/airports.dat"
ROUTES_FILE = "data/routes.dat"
AIRPORTS_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
ROUTES_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"


# --------------- Downloading ------------

def download_dataset():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(AIRPORTS_FILE):
        urllib.request.urlretrieve(AIRPORTS_URL, AIRPORTS_FILE)
    if not os.path.exists(ROUTES_FILE):
        urllib.request.urlretrieve(ROUTES_URL, ROUTES_FILE)


# ----------------- Parsing -----------------

def read_airports_file():
    airport_data = {}

    with open(AIRPORTS_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) >= 8:
                airport_code = row[4]
                lat = row[6]
                lon = row[7]
                airport_data[airport_code] = (lat, lon)

    return airport_data


def read_routes_file():
    route_data = []

    with open(ROUTES_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6:
                source_airport = row[2]
                destination_airport = row[4]
                route_data.append((source_airport, destination_airport))

    return route_data


# ------------------ Cleaning --------------------

def clean_airport_data(raw_airport_data):
    cleaned_airports = {}

    for airport_code in raw_airport_data:
        if airport_code == "\\N":
            continue

        lat, lon = raw_airport_data[airport_code]

        try:
            lat = float(lat)
            lon = float(lon)
            cleaned_airports[airport_code] = (lat, lon)
        except ValueError:
            continue

    return cleaned_airports


def calculate_distance_km(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


def build_weighted_edges(route_data, airport_data):
    edges = []
    seen_routes = set()

    for source_airport, destination_airport in route_data:
        if source_airport == "\\N" or destination_airport == "\\N":
            continue
        if source_airport not in airport_data or destination_airport not in airport_data:
            continue
        if source_airport == destination_airport:
            continue
        if (source_airport, destination_airport) in seen_routes:
            continue

        seen_routes.add((source_airport, destination_airport))

        lat1, lon1 = airport_data[source_airport]
        lat2, lon2 = airport_data[destination_airport]

        distance_km = calculate_distance_km(lat1, lon1, lat2, lon2)
        edges.append((source_airport, destination_airport, distance_km))

    return edges


def load_graph_edges():
    download_dataset()

    raw_airports = read_airports_file()
    raw_routes = read_routes_file()

    cleaned_airports = clean_airport_data(raw_airports)
    edges = build_weighted_edges(raw_routes, cleaned_airports)

    return edges


if __name__ == "__main__":
    edges = load_graph_edges()
    print("Number of edges:", len(edges))