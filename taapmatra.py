from configparser import ConfigParser
import argparse

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

if __name__ == "__main__":
    user_args = get_args_from_user()
