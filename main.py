from twilio.rest import Client
import requests
import os

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
client = Client(ACCOUNT_SID, AUTH_TOKEN)
TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]

MY_LAT = "41.917179"
MY_LONG = "3.163800"
API_KEY = os.environ["OPEN_WEATHER_API"]


def is_going_to_rain(lat: str, lon: str, appikey: str) -> bool:
    """Checks if it will rain in the next three hours."""
    rain_condition = 700

    parameters = {
        "lat": f"{lat}",
        "lon": f"{lon}",
        "appid": f"{appikey}"
    }
    URL = "https://api.openweathermap.org/data/2.5/forecast"

    weather_response = requests.request("GET", url=URL, params=parameters)
    data = weather_response.json()["list"][:12]
    weather_next_twelve_hours = [weather["weather"][0]["id"] for weather in data]

    for weather in weather_next_twelve_hours:
        if weather <= rain_condition:
            return True


if is_going_to_rain(lat=MY_LAT, lon=MY_LONG, appikey=API_KEY):
    message = client.messages.create(body="Rain Alert! It's about to rain. Don't forget to pick the umbrella☂",
                                     from_=f"{TWILIO_PHONE_NUMBER}",
                                     to="")
