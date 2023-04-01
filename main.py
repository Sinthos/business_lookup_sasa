import requests
import csv
import time

# Function to search for nearby places based on the given parameters
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

# Function to retrieve details about a place using its place_id
def get_place_details(api_key, place_id):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number",
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    return response.json()

# Function to save the collected results to a CSV file
def save_to_csv(results, api_key, file_name):
    with open(file_name, "w", encoding="utf-8", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Address", "Phone Number"])

        for result in results:
            name = result["name"]
            address = result["vicinity"]
            place_id = result["place_id"]

            details = get_place_details(api_key, place_id)
            phone_number = details.get("result", {}).get("formatted_phone_number", "Not available")

            csv_writer.writerow([name, address, phone_number])

# Main program
if __name__ == "__main__":
    API_KEY = input("Enter your API Key: ")
    LOCATION = input("Enter the coordinates (latitude,longitude): ")
    RADIUS = int(input("Enter the search radius (in meters): "))
    KEYWORD = input("Enter the keyword: ")
    PLACE_TYPE = input("Enter the place type: ")

    latitude, longitude = LOCATION.split(',')
    first_two_digits_latitude = latitude[:2]
    first_two_digits_longitude = longitude[:2]

    CSV_FILE_NAME = f"{first_two_digits_latitude}_{first_two_digits_longitude}_{KEYWORD}_{PLACE_TYPE}.csv"

    all_results = []
    next_page_token = None

    # Loop to fetch all result pages
    while True:
        results = search_nearby_places(API_KEY, LOCATION, RADIUS, KEYWORD, PLACE_TYPE, next_page_token)
        all_results.extend(results["results"])

        next_page_token = results.get("next_page_token")
        if next_page_token:
            time.sleep(10)  # Google Maps Places API delay between consecutive requests
        else:
            break

    save_to_csv(all_results, API_KEY, CSV_FILE_NAME)
    print(f"The results have been saved in the file {CSV_FILE_NAME}.")
