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
        print("ho get_city_time")
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


def print_formatted_time(time, city=None):
    if time == None:
        return
    formatted_time = time.strftime("%A, %B %d, %Y, %I:%M %p")
    if city == None:
        print(f"Your current date and time: {formatted_time}")
    else:
        print(f"Date and time in {city}: {formatted_time}")


def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]['humidity']
        return f"The weather in {city} is {weather_description} with a temperature of {temperature}K and humidity of {humidity}% "


api_key = "a487fc0204a87a86407718349acc41ef"
while True:
    city = input("Enter the city name: ")
    weather = get_weather(city, api_key)
    if weather != None:
        print(weather)
        print_formatted_time(get_city_time(city), city)
        print_formatted_time(get_user_time())
        # print(get_city_time(city))
        break
    else:
        print("City not found, Please enter a valid city name.")
