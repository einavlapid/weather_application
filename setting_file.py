import json
import pandas as pd
import ipdb

class SettingFile:
    FILE_NAME = "data.json"
    CITIES_DATASET_FILE = "common_cities.csv"
    DEFAULT_CITY = "default_city"
    USER_CITY = "user_city"
    COMMON_LOCATIONS = "common_locations"
    TEMERATURE_UNIT = "temperature_unit"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"

    default_temperature_units = None
    common_cities = None
    file_settings = {}

    def __init__(self):
        self.file_settings = {}
        self.common_cities = []

    def get_default_city(self):
        return self.file_settings.get(self.DEFAULT_CITY, "")

    def get_user_city(self):
        return self.file_settings.get(self.USER_CITY, "")
    def get_default_city_index(self):
        if self.file_settings.get(self.DEFAULT_CITY, "") in self.common_cities != "":
            return self.common_cities.index(self.file_settings.get(self.DEFAULT_CITY, ""))
        else:
            return 0

    def get_city_index(self, city):
        if city in self.common_cities != "":
            return sorted(self.common_cities).index(city)
        else:
            return 0

    def read_settings(self):
        self.common_cities = []
        self.file_settings = {}

        with open(self.FILE_NAME, 'r') as file:
            self.file_settings = json.load(file)
        self.default_temperature_units = self.file_settings.get(self.TEMERATURE_UNIT, "")
        self.common_cities = self.file_settings.get(self.COMMON_LOCATIONS, [])
        default_city = self.file_settings.get(self.DEFAULT_CITY, "")
        if default_city != "" and default_city not in self.common_cities:
            self.common_cities.append(default_city)
        user_city = self.file_settings.get(self.USER_CITY, "")
        if user_city != "" and user_city not in self.common_cities:
            self.common_cities.append(user_city)

        self.common_cities = sorted(self.common_cities)
    def save_settings(self,default_city, user_city, temperature_units, common_cities = []):
        if common_cities != []:
            self.common_cities = sorted(common_cities)

        self.file_settings[self.DEFAULT_CITY] = default_city
        self.file_settings[self.USER_CITY] = user_city
        self.file_settings[self.TEMERATURE_UNIT] = temperature_units
        self.default_temperature_units = temperature_units
        if default_city not in self.common_cities:
            self.common_cities.append(default_city)
        if user_city not in self.common_cities:
            self.common_cities.append(user_city)
        self.common_cities = sorted(self.common_cities)
        self.file_settings[self.COMMON_LOCATIONS] = self.common_cities

        with open(self.FILE_NAME, 'w') as file:
            json.dump(self.file_settings, file)


