CLI weather app made in Python.

initial specifications of the weather app : The intention is that the weather
app will

- Take a city name as required input.
- Take an optional flag to display the temperature in Farenheit instead of
  Celsius, if required.
- Call an online weather API to fetch the weather data.
- Display the city name, current weather conditions, and the current temperature.
- Format the output visually using colours, spacing and emojis.

Learning outcomes :
- How to get access to the API key for the API endpoint of openweather
- How to use configparser to handle configuration files (to store the API key
  in this case.)
- How to use argparse.
- How to make a request using urllib to get the response from the website.
- Handling a bunch of exceptions.
- Building a display function using ANSI escape codes.
- Styling using emojis.
