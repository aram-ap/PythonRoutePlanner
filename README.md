# Route Optimizer

This Python script calculates the best route between multiple destinations, optionally starting from a specified origin or using the user's current location. It leverages the Google Maps Directions API to provide detailed directions and estimated travel times, while avoiding highways to potentially bypass restricted roads.

## Features

-  Calculate optimized routes between multiple destinations.
-  Use a specified starting location or automatically detect the current location.
-  Display step-by-step directions and estimated travel times.
-  Provide alternative routes for manual selection.
-  Avoid highways to reduce the likelihood of using restricted roads.

## Requirements

-  Python 3.x
-  Google Maps API key
-  Internet connection

## Setup

1. **Clone the Repository**

   Clone this repository to your local machine using:

   ```bash
   git clone https://github.com/aram-ap/PythonRoutePlanner.git
   ```

2. **Install Dependencies**

   Navigate to the project directory and install the required Python packages:

   ```bash
   cd PythonRoutePlanner
   pip install -r requirements.txt
   ```

   Ensure `requirements.txt` contains:
   ```plaintext
   requests
   python-dotenv
   argparse
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the project directory and add your Google Maps API key:

   ```plaintext
   GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key
   ```

## Usage

Run the script with the following command:

```bash
python run.py [--origin "Starting Address"]
```

-  `--origin "Starting Address"`: (Optional) Specify the starting location address. If not provided, the script will attempt to use the current location.

### Example

```bash
python run.py --origin "1234 Elm St, Springfield"
```

Or, to use the current location:

```bash
python run.py
```

When prompted, enter your destinations as a comma-separated list:

```
Enter your destinations separated by commas: 26877 Tourney Rd Santa Clarita CA, 26455 Rockwell Canyon Rd Santa Clarita CA, 26468 Carl Boyer Dr Santa Clarita CA, 22913 Soledad Canyon Rd
```

## Output

The script will display the best route with detailed directions and estimated travel times. It will also provide alternative routes for manual selection.

## Notes

-  Ensure you have a valid Google Maps API key with access to the Directions API.
-  Be aware of the API usage limits to avoid additional charges.
-  The script attempts to avoid highways, which may help in bypassing restricted roads, but it cannot guarantee avoidance of all restricted areas.

