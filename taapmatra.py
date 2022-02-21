from urllib import error, parse, request
from configparser import ConfigParser
import argparse
import json
import sys

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def _get_api_key():

    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

def get_args_from_user():

    parser = argparse.ArgumentParser()

    parser.add_argument("city", nargs="+", default=None, help="enter city name")

    parser.add_argument("-i", "--imperial", action="store_true",
            help="display the temperature in imperial units")

    return parser.parse_args()

def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to Openweather's weather API

    :city_input: The name of the city as a list of strings.
    :imperial: Boolean argument to specify if output is in imperial units.
    :returns: The url as a string.

    """
    api_key               = _get_api_key()
    city_name             = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units                 = "imperial" if imperial else "metric"
    url                   = (f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
                            f"&units={units}&appid={api_key}")

    return url

def get_weather_data(query_url):
    """Make an http request to the openweather API and return the response as a
    Python object.

    :query_url: URL formatted for openweather's city name endpoint.
    :returns: A dictionary containing the information for a particular city.

    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: # Auth problem
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404: # Resource not found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong. HTTP error code : {http_error.code}")

    data = response.read()

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")

def display_weather_info(weather_data, imperial=False):
    """Prints formatted weather information about a city.

    :weather_data: weather data in the form of a Python dictionary.
    :imperial: Whether or not user wants information in imperial units.
    :returns: None. Just displays the information to the console.

    """
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    print(f"{city}", end="")
    print(f"\t{weather_description.capitalize()}", end=" ")
    print(f"({temperature}°{'F' if imperial else 'C'})")

if __name__ == "__main__":
    user_args    = get_args_from_user()
    query_url    = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)

    display_weather_info(weather_data, user_args.imperial)
