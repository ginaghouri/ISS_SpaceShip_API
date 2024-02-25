# Requirements 6,8: Inbuilt functions, import these modules if needed
import json
import requests
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
from time import sleep


# Function to fetch ISS location data from the API
# Requirement 7: Use a free API: no need to set up any keys

def fetch_iss_location():
    url = "http://api.open-notify.org/iss-now.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch ISS location data: {e}")
        return None


# Requirement 4: Use functions with returns to make code reusable
# Function1 to get coordinates for a user-specified location

def get_coordinates_for_location(location_name):
    geolocator = Nominatim(user_agent="iss-tracker")
    location = geolocator.geocode(location_name)

    if location:
        return location.latitude, location.longitude
    else:
        print(f"Could not find coordinates for '{location_name}'")
        return None, None


# Requirement 10 Creative Problem:
# function2 to calculate the distance between two sets of coordinates (Haversine-ref.Wikipedia)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_km = earth_radius * c

    return distance_km


# Welcome Message
print("Welcome to the International Space Station App!")

# Ask the user for their email and set it as the user-agent
user_email = input("Please enter your email: ").strip()
geolocator = Nominatim(user_agent=user_email)

# Requirement 3: Use a while loop to avoid repetition
# Requirement 1A: Use boolean values to branch logic of app
exitApp = False
while not exitApp:
    # Fetch ISS location data
    iss_data = fetch_iss_location()

    if iss_data:
        iss_latitude = float(iss_data["iss_position"]["latitude"])
        iss_longitude = float(iss_data["iss_position"]["longitude"])

        # Get a user-specified location
        user_location_name = input("Enter a location (country or city): ").strip()

        # Requirement 5: Use string slicing
        # Slice the user's input to the first 50 characters to prevent very long queries
        user_location_name = user_location_name[:50]

        user_latitude, user_longitude = get_coordinates_for_location(user_location_name)

        if user_latitude is not None and user_longitude is not None:
            # Requirement 10 Creative Scenario: Calculate the distance between the ISS and the user's location
            distance_km = calculate_distance(iss_latitude, iss_longitude, user_latitude, user_longitude)

            # Perform reverse geocoding to get the country over which the ISS is flying
            location = geolocator.reverse(f"{iss_latitude}, {iss_longitude}", language='en')

            if location and 'address' in location.raw:
                # Try to get the country name from the location data
                iss_country = location.raw['address'].get('country', 'Unknown')
            else:
                # If country information is not available, set it to 'Unknown'
                iss_country = 'Unknown'

            print(f"The ISS is approximately {distance_km:.2f} kilometers away from {user_location_name}")
            print(f"The ISS is currently flying over {iss_country}\n")

            # Requirement 2: Use a data structure (dictionary) to store values
            result = {
                "ISS_Location": {"Latitude": iss_latitude, "Longitude": iss_longitude},
                "User_Location": {"Name": user_location_name, "Latitude": user_latitude, "Longitude": user_longitude},
                "Distance_km": distance_km,
                "ISS_Country": iss_country
            }

            # Requirement 9: Write final results in a file
            with open("iss_landmark_results.json", "w") as file:
                json.dump(result, file, indent=4)

            again = input("Do you want to check another location? ('n' to exit): ")
            # Requirement 1B: Use if-else statements to branch logic of the program
            if again == 'n':
                print('Thank you for using the ISS App!')
                exitApp = True
                break  # Exit the loop when 'n' is pressed

        else:
            print("Couldn't fetch data from Geopy API. Exit App...")
    else:
        print("Couldn't fetch data from ISS API. Exit App...")

# The program will exit after the user presses 'n' and won't continue to fetch ISS location

#Unique Problem: geocoding services, like Nominatim, may have limitations on the number of requests you can make in a given time period.
     

