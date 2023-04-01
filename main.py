import requests
import csv
import time

# Funktion, um nahe gelegene Orte basierend auf den angegebenen Parametern zu suchen
def search_nearby_places(api_key, location, radius, keyword, place_type, next_page_token=None):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": location,
        "radius": radius,
        "type": place_type,
        "keyword": keyword,
        "key": api_key,
    }

    if next_page_token:
        params["pagetoken"] = next_page_token

    response = requests.get(base_url, params=params)
    return response.json()

# Funktion, um Details zu einem Ort anhand seiner place_id abzurufen
def get_place_details(api_key, place_id):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number",
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    return response.json()

# Funktion, um die gesammelten Ergebnisse in eine CSV-Datei zu speichern
def save_to_csv(results, api_key, file_name):
    with open(file_name, "w", encoding="utf-8", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Adresse", "Telefonnummer"])

        for result in results:
            name = result["name"]
            address = result["vicinity"]
            place_id = result["place_id"]

            details = get_place_details(api_key, place_id)
            phone_number = details.get("result", {}).get("formatted_phone_number", "Nicht verfügbar")

            csv_writer.writerow([name, address, phone_number])

# Hauptprogramm
if __name__ == "__main__":
    API_KEY = "YOUR_API_KEY"  # YOUR_API_KEY durch den API-Schlüssel ersetzen
    LOCATION = "49.00,7.00"  # Koordinaten um die gesucht werden soll
    RADIUS = 20000  # Suche im Umkreis von 20 km
    KEYWORD = "italienisch"
    PLACE_TYPE = "restaurant"
    CSV_FILE_NAME = "italienische_restaurants.csv"

    all_results = []
    next_page_token = None

    # Schleife, um alle Ergebnisseiten abzurufen
    while True:
        results = search_nearby_places(API_KEY, LOCATION, RADIUS, KEYWORD, PLACE_TYPE, next_page_token)
        all_results.extend(results["results"])

        next_page_token = results.get("next_page_token")
        if next_page_token:
            time.sleep(10)  # Google Maps Places API Verzögerung zwischen aufeinanderfolgenden Anfragen
        else:
            break

    save_to_csv(all_results, API_KEY, CSV_FILE_NAME)
    print(f"Die Ergebnisse wurden in der Datei {CSV_FILE_NAME} gespeichert.")
