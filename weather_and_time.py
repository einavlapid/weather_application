import requests
import geocoder
from geopy.geocoders import Photon
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz


def get_city_time(city):
    geolocator = Photon(user_agent="measurements")
    location = geolocator.geocode(city)
    if location:
        return get_time(location.latitude, location.longitude)


def get_user_time():
    g = geocoder.ip('me')
    return get_time(g.latlng[0], g.latlng[1])


def get_time(latitude, longitude):
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=longitude, lat=latitude)
    timezone = pytz.timezone(timezone)
    time = datetime.now(timezone)
    return time


def get_formatted_time(time, city=None):
    if time == None:
        return
    formatted_time = time.strftime("%A, %B %d, %Y, %I:%M %p")
    if city == None:
        return f"Your current date and time: {formatted_time}"
    else:
        return f"Date and time in {city}: {formatted_time}"


def get_weather(city, api_key, temperature_unit):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        temperature_unit_sign = "K"
        if temperature_unit == 'C':
            temperature = temperature -273.15
            temperature_unit_sign = "°C"

        elif temperature_unit == 'F':
            temperature = ((temperature * 9)/5) -459.67
            temperature_unit_sign = "°F"

        humidity = data["main"]['humidity']
        return f"The weather in {city} is {weather_description} with a temperature of {int(temperature)} {temperature_unit_sign} and humidity of {humidity}% "
        # return f"The weather in {city} is {weather_description} with a temperature of {temperature}K and humidity of {humidity}% "


