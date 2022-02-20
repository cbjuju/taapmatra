from urllib import parse, request
from configparser import ConfigParser
import argparse
import json

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
    response = request.urlopen(query_url)
    data = response.read()
    return json.loads(data)

if __name__ == "__main__":
    user_args    = get_args_from_user()
    query_url    = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    print(weather_data)
