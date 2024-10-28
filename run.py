import requests
from dotenv import load_dotenv
import os
import argparse

def get_current_location():
    """Get the current location of the user using ipinfo.io."""
    try:
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            data = response.json()
            loc = data.get('loc')  # Format is 'latitude,longitude'
            return loc
        else:
            print("Failed to get location data from ipinfo.io")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_address_from_coordinates(api_key, coordinates):
    """Get the street address from latitude and longitude using Google Maps Geocoding API."""
    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json?"
        f"latlng={coordinates}&key={api_key}"
    )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK' and data['results']:
                return data['results'][0]['formatted_address']
            else:
                print("Could not find an address for the given coordinates.")
                return None
        else:
            print("Failed to connect to the Geocoding API. Status code:", response.status_code)
            return None
    except Exception as e:
        print(f"An error occurred while fetching the address: {e}")
        return None

def get_best_route(api_key, origin, destinations):
    # Build the destinations string for the API request
    destinations_str = '|'.join(destinations)

    # Construct the request URL with alternatives
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={origin}&"
        f"destination={origin}&"  # Return to the origin
        f"waypoints=optimize:true|{destinations_str}&"
        f"avoid=highways&"  # Avoid highways as a proxy for restricted roads
        f"alternatives=true&"  # Request alternative routes
        f"key={api_key}"
    )

    # Send the request to the Google Maps Directions API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        directions = response.json()

        # Check if the API returned a valid response
        if directions['status'] == 'OK':
            routes = directions['routes']

            # Iterate over each route and display details
            for idx, route in enumerate(routes):
                print(f"\nRoute {idx + 1}:")
                waypoint_order = route['waypoint_order']

                # Create an ordered list of destinations
                ordered_destinations = [destinations[i] for i in waypoint_order]

                # Include the origin at the start and end
                ordered_destinations.insert(0, origin)
                ordered_destinations.append(origin)

                # Extract durations, distances, and steps
                leg_durations = []
                total_duration = 0
                all_steps = []
                for leg in route['legs']:
                    duration = leg['duration']['text']
                    total_duration += leg['duration']['value']  # in seconds
                    leg_durations.append(duration)

                    steps = []
                    for step in leg['steps']:
                        instructions = step['html_instructions']
                        steps.append(instructions)
                    all_steps.append(steps)

                # Convert total duration to hours and minutes
                total_hours, remainder = divmod(total_duration, 3600)
                total_minutes = remainder // 60

                # Print the route details
                for i, place in enumerate(ordered_destinations[:-1]):
                    print(f"From {place} to {ordered_destinations[i+1]}: {leg_durations[i]}")
                    print("Directions:")
                    for step in all_steps[i]:
                        # Remove HTML tags for clean printing
                        clean_step = step.replace('<b>', '').replace('</b>', '').replace('<div style="font-size:0.9em">', ' ').replace('</div>', '')
                        print(f"  - {clean_step}")
                    print()

                print(f"Total travel time for Route {idx + 1}: {total_hours} hours and {total_minutes} minutes")

            return routes
        else:
            print("Error:", directions['status'])
            return None
    else:
        print("Failed to connect to the API. Status code:", response.status_code)
        return None

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Your Google Maps API key from the environment variable
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    if not api_key:
        print("API key not found. Please set it in the .env file.")
        return

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Calculate the best route between destinations.")
    parser.add_argument('--origin', type=str, help='Specify the starting location address.')
    args = parser.parse_args()

    # Determine the starting location
    if args.origin:
        origin = args.origin
        print(f"Using specified start location: {origin}")
    else:
        origin = get_current_location()
        if origin:
            address = get_address_from_coordinates(api_key, origin)
            if address:
                print(f"Your current location is: {address}")
        else:
            print("Could not determine your current location.")
            return

    # Prompt the user to input destinations
    destinations_input = input("Enter your destinations separated by commas: ")
    destinations = [dest.strip() for dest in destinations_input.split(',') if dest.strip()]

    if not destinations:
        print("No destinations entered. Please run the script again and enter at least one destination.")
        return

    # Get the best route
    routes = get_best_route(api_key, origin, destinations)

    if routes:
        print("\nPlease review the routes above and select one that best avoids restricted roads.")

if __name__ == '__main__':
    main()

