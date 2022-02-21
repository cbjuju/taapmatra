from urllib import error, parse, request
from configparser import ConfigParser
import argparse
import json
import sys
import style

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE      = range(300, 400)
RAIN         = range(500, 600)
SNOW         = range(600, 700)
ATMOSPHERE   = range(700, 800)
CLEAR        = range(800, 801)
CLOUDY       = range(801, 900)

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

def _select_weather_display_params(weather_id):
    """ To enter the unicode symbols in the following, press Ctrl-V in insert
    mode followed by the unicode code point, taking care of the case of the
    letters in the code point and ignoring the plus sign. In this case I just
    copied and pasted the symbols in from the internet. """
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.WHITE)
    else: 
        display_params = ("🌈", style.RESET)
# In case the API adds new weather codes
    return display_params

def display_weather_info(weather_data, imperial=False):
    """Prints formatted weather information about a city.

    :weather_data: weather data in the form of a Python dictionary.
    :imperial: Whether or not user wants information in imperial units.
    :returns: None. Just displays the information to the console.

    """
    city = weather_data["name"]
    weather_id = weather_data["weather"][0]["id"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)

    weather_symbol, color = _select_weather_display_params(weather_id)

    style.change_color(color)
    print(f"\t{weather_symbol}", end="")
    print(f"{weather_description.capitalize():^{style.PADDING}}", end=" ")
    style.change_color(style.RESET)

    print(f"({temperature}°{'F' if imperial else 'C'})")

if __name__ == "__main__":
    user_args    = get_args_from_user()
    query_url    = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)

    display_weather_info(weather_data, user_args.imperial)
