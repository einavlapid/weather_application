

from setting_file import SettingFile
import os
import sys
import ipdb

class MainStreamlitwin:
    import streamlit as st
    import weather_and_time as wt
    API_KEY = "a487fc0204a87a86407718349acc41ef"
    sf = SettingFile()
    city_weather_result = ""
    get_weather_btn = None
    selected_city = None
    title = None
    def __init__(self):
        self.sf.read_settings()


    def user_setting_streamlit(self):
        self.st.title("User settings")
        default_city = self.st.text_input("Default city:",self.sf.get_default_city(),key="Default_city")
        user_city = self.st.text_input("User city:", self.sf.get_user_city(),key="user_city")
        if self.sf.default_temperature_units == self.sf.FAHRENHEIT:
            selected_temperature_units = self.st.selectbox('Select temerature unit', [self.sf.CELSIUS, self.sf.FAHRENHEIT], index=1, key= "selected_temperature_units")
        else:
            selected_temperature_units = self.st.selectbox('Select temerature unit', [self.sf.CELSIUS, self.sf.FAHRENHEIT], index=0, key="selected_temperature_units")

        col1, col2 = self.st.columns((5, 1))
        with col1:
            if "updated_location" in self.st.session_state:
                default_locations = self.st.multiselect("Location list:", sorted(self.st.session_state.updated_location),
                                                  key="multiselect_key")
            else:
                default_locations = self.st.multiselect("Location list:", sorted(self.sf.common_cities),key="multiselect_key")

        with col2:
            del_locations = self.st.button("Delete Selected")
            if default_locations and del_locations:
                updated_locations = sorted([value for value in self.sf.common_cities if value not in default_locations])
                self.sf.common_cities = updated_locations
                default_locations = []
                self.st.session_state.updated_location = updated_locations
                self.sf.save_settings(default_city, user_city, selected_temperature_units, self.sf.common_cities)
                self.st.rerun()


        col1, col2 = self.st.columns((5, 1))
        with col1:
            locations = self.st.text_input(
                "Add\Delete locations (Example: new york, tel aviv, london):",
                 placeholder="Add locations (Example: new york, tel aviv, london):",
                 label_visibility='collapsed')
        with col2:
            add_locations = self.st.button("Add")
            if add_locations and locations:
                locations_list = locations.split(",")
                for location in locations_list:
                    location = location.lstrip()
                    if location not in self.sf.common_cities:
                        self.sf.common_cities.append(location)
                locations = ""
                updated_locations = self.sf.common_cities
                self.st.session_state.updated_location = updated_locations
                self.sf.save_settings(default_city, user_city, selected_temperature_units, self.sf.common_cities)
                self.st.rerun()


        save_changes = self.st.button("Save changes")

        if save_changes:
            self.sf.save_settings(default_city, user_city, selected_temperature_units, self.sf.common_cities)



    def weather_win(self):
        self.sf.read_settings()
        self.st.title("Welcome to Weather application")
        default_city_index = self.sf.get_default_city_index()
        if default_city_index == -1:
            default_city_index = 0
        selected_city = self.st.selectbox('Select a city', self.sf.common_cities, index=default_city_index)
        if selected_city:
            weather = self.wt.get_weather(selected_city, self.API_KEY, str(self.sf.default_temperature_units)[0])
            if weather:
                self.st.write(weather)
                city_time = self.wt.get_formatted_time(self.wt.get_city_time(selected_city), selected_city)
                self.st.write(city_time)
                user_time = self.wt.get_formatted_time(self.wt.get_user_time())
                self.st.write(user_time)
            else:
                self.st.write("City not found, Please enter a valid city name.")

    def open_main_win(self):
        menu_selection = self.st.sidebar.radio("Go to", ["Weather application", "User setting"], index=0)
        if menu_selection == "Weather application":
            self.weather_win()
        elif menu_selection == "User setting":
            self.user_setting_streamlit()

