import requests
from .models import BusStations

def datafill():

    url = "https://testapi.daewoo.net.pk/api/schedule/getDepartures"  # Replace with your actual endpoint URL
    headers = {
        "x-client_id": "DES-0000",  # Replace with your actual client ID
        "x-client_password": "$desTination71024021"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for station_data in data["Data"]:
            terminal_code = station_data["TERMINAL_CODE"]
            terminal_name = station_data["TERMINAL_NAME"]

            # Check if a station with the same terminal code already exists
            existing_station = BusStations.objects.filter(terminal_code=terminal_code).first()

            if existing_station:
                # Update the existing station if necessary
                existing_station.terminal_name = terminal_name
                existing_station.save()
            else:
                # Create a new station if it doesn't exist
                BusStations.objects.create(terminal_name=terminal_name, terminal_code=terminal_code)

        print("Data has been successfully saved.")
    else:
        print("Failed to fetch data from the endpoint. Status code:", response.status_code)
    return "Done"