
import user_settings as us
import weather_and_time as wt
from user_settings import UserSetting
from setting_file import SettingFile
import tkinter as tk
from tkinter import ttk
import threading
import ipdb

class Mainwin:
    API_KEY = "a487fc0204a87a86407718349acc41ef"
    us = UserSetting()
    sf = SettingFile()
    city_combobox = None
    root = None
    city_weather_result = None
    get_weather_btn = None

    def __init__(self):
        self.sf.read_settings()

    def open_user_settings(self):
        self.us.settings_window_counter
        if self.us.settings_window_counter == 0:
            self.us.settings_window_counter = 1
            self.us.display_setting_window(self.root, self.sf)


    def get_weather_btn(self):
        self.city_combobox.config(state=tk.DISABLED)
        self.get_weather_btn.config(state=tk.DISABLED)
        self.root.config(cursor="watch")
        self.root.update()
        thread = threading.Thread(target=self.get_weather_data)
        thread.start()
    def get_weather_data(self):
        city = self.city_combobox.get()
        if city == "":
            return
        self.sf.read_settings()
        weather = wt.get_weather(city, self.API_KEY, str(self.sf.default_temperature_units)[0])
        if weather != None:
            city_time = wt.get_formatted_time(wt.get_city_time(city), city)
            user_city = self.sf.get_user_city()
            user_time = wt.get_formatted_time(wt.get_city_time(user_city), user_city) if user_city != "" else wt.get_formatted_time(wt.get_user_time())
            self.city_weather_result["text"] = f"{weather}\n {city_time}\n{user_time}"
            self.city_weather_result.anchor = tk.W
        else:
            self.city_weather_result["text"] = "City not found, Please enter a valid city name."
            self.city_weather_result.anchor = tk.W

        self.get_weather_btn.config(state=tk.NORMAL)
        self.city_combobox.config(state=tk.NORMAL)
        self.root.config(cursor="")  # Reset cursor to default
        self.root.update()

    def city_combolist_opened(self,event):
        self.sf.read_settings()
        self.city_combobox['values'] = sorted(self.sf.common_cities)

    def open_main_win(self):
        self.root = tk.Tk()
        self.root.title("Weather application")

        city_label = tk.Label(self.root, text="Enter the city name", anchor=tk.W, font=("Arial", 20), bg="lightblue", fg="navy")
        city_label.pack(side=tk.TOP,padx=10, pady=10)

        self.city_combobox = ttk.Combobox(self.root, values=sorted(self.sf.common_cities))
        self.city_combobox.pack(side=tk.TOP, padx=10, pady=10)
        default_city = self.sf.file_settings.get(self.sf.DEFAULT_CITY, "")
        if default_city != "" and default_city in self.sf.common_cities:
                default_index = self.sf.common_cities.index(default_city)
                self.city_combobox.current(default_index)
        self.city_combobox.bind("<FocusIn>", self.city_combolist_opened)

        self.get_weather_btn = tk.Button(self.root, text="Go", font=("Arial", 12), bg="skyblue", fg="navy", relief=tk.RAISED, bd=2,command=self.get_weather_btn)
        self.get_weather_btn.pack(side=tk.TOP,padx=10, pady=10)
        # Response label
        self.city_weather_result = tk.Label(self.root, text="", anchor=tk.W ,justify=tk.LEFT, bg="lightblue")
        self.city_weather_result.pack(side=tk.TOP, padx=10, pady=10)

        user_settings = tk.Button(self.root, text="User setting", font=("Arial", 12), bg="skyblue", fg="navy", relief=tk.RAISED, bd=2,command=self.open_user_settings)
        user_settings.pack(side=tk.LEFT,padx=10, pady=10)

        self.root.configure(bg="lightblue")
        self.root.geometry("600x300")
        self.root.mainloop()

