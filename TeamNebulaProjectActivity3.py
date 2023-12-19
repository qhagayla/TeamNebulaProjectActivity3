import urllib.parse
import requests
from tabulate import tabulate
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "7RaN1Tvl9VzAd4dUGM6WHVH9mp3go3Q2"
fuel_efficiency = 10  # Example fuel efficiency in liters per kilometer
average_speed = 60  # Example average speed in kilometers per hour

while True:
    orig = input("Starting Location: ")
    if orig.lower() in {"quit", "q"}:
        break
    dest = input("Destination: ")
    if dest.lower() in {"quit", "q"}:
        break
    units = input("Enter units (km/miles): ").lower()

    # Allow users to choose between the fastest and shortest routes
    route_type = input("Choose route type (fastest/shortest): ").lower()

    url_params = {
        "key": key,
        "from": orig,
        "to": dest,
        "routeType": route_type,  # Added route type parameter
    }

    url = main_api + urllib.parse.urlencode(url_params)
    json_data = requests.get(url).json()

    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("API Status: " + Fore.GREEN + str(json_status) + " = A successful route call.\n")

        # Display route information
        print("=============================================")
        print("Directions from " + Fore.CYAN + orig + Fore.RESET + " to " + Fore.CYAN + dest + Fore.RESET)
        print("Trip Duration:   " + Fore.YELLOW + json_data["route"]["formattedTime"])

        if units == "miles":
            distance = json_data["route"]["distance"]
            fuel_unit = "miles"
        else:
            distance = json_data["route"]["distance"] * 1.61
            fuel_unit = "km"

        print(f"{('Distance:'): <15} {distance:.2f} {fuel_unit}")

        # Compute fuel used based on distance and average speed
        trip_duration_hours = json_data["route"]["time"] / 3600
        fuel_used = distance / fuel_efficiency
        print(f"{('Fuel Used:'): <15} {fuel_used:.2f} Ltr")

        print("=============================================")

        # Display turn-by-turn directions in a table
        directions_table = []
        for maneuver in json_data["route"]["legs"][0]["maneuvers"]:
            direction = maneuver["narrative"]
            distance = maneuver["distance"] * 1.61 if units == "km" else maneuver["distance"]
            directions_table.append([direction, f"{distance:.2f} {fuel_unit}"])

        print(tabulate(directions_table, headers=["Direction", "Distance"], tablefmt="fancy_grid"))
        print("=============================================\n")

        # Display alternative routes
        if "route" in json_data and "alternateRoutes" in json_data["route"]:
            print("Alternative Routes:")
            for i, route in enumerate(json_data["route"]["alternateRoutes"], start=1):
                print(f"Route {i}:")
                print(f"   Duration: {route['formattedTime']}")
                print(f"   Distance: {route['distance']:.2f} {fuel_unit}")
                print("=============================================")

    elif json_status == 402:
        print(Fore.RED + "**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print(Fore.RED + "**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print(Fore.RED + "************************************************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")
