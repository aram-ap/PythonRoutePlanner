import requests
from dotenv import load_dotenv
import os

def get_current_location():
    """Get the current location of the user using geopy."""

    try:
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            data = response.json()
            loc = data.get('loc') # Format is 'latitude, longitude'
            return loc
        else:
            print("Failed to get location data from ipinfo.io")
            return None
    except Exception as e:
        print(f"An error occured: {e}")
        return None

def get_best_route(api_key, origin, destinations):
    # Build the destinations string for the API request
    destinations_str = '|'.join(destinations)

    # Construct the request URL
    url = (
            f"https://maps.googleapis.com/maps/api/directions/json?"
            f"origin={origin}&"
            f"destination={origin}&" # Return to the origin
            f"waypoints=optimize:true|{destinations_str}&"
            f"key={api_key}"
            )

    # Send the request to the Google Maps Directions API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        directions = response.json()

        # Check if the API returned a valid response
        if directions['status'] == 'OK':
            route = directions['routes'][0]

            # Extract the waypoint order
            waypoint_order = route['waypoint_order']

            # create an ordered list of destinations
            ordered_destinations = [destinations[i] for i in waypoint_order]

            # Include the origin at the start and end
            ordered_destinations.insert(0, origin)
            ordered_destinations.append(origin)

            return ordered_destinations
        else:
            print("Error:", directions['status'])
            return None
    else:
        print("Failed to connect to the API. Status code:", response.status_code)
        return None

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Goodle Maps API key from the .env file
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    if not api_key:
        print("API key not found. Please set it in the .env file.")
        return

    # Attempt to get user's current Location
    current_location = get_current_location()

    # Define a default location if current location is not available
    default_location = 'Santa Clarita, CA'

    # Use the current location if available, otherwise use the default location
    origin = current_location if current_location else default_location

    # Prompt the user to input destinations
    destinations_input = input("Enter your destinations separated by commas: ")
    destinations = [dest.strip() for dest in destinations_input.split(',') if dest.strip()]

    if not destinations:
        print("No destinations entered. Please run the script again and enter at least one destination.")
        return

    # Get best route
    best_route = get_best_route(api_key, origin, destinations)

    if best_route:
        print("Best route to visit all destinations:")
        for place in best_route:
            print(place)

if __name__ == '__main__':
    main()


