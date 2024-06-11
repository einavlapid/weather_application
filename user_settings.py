import tkinter as tk
from tkinter import ttk
from setting_file import SettingFile
# from main_win import Mainwin

class UserSetting:
    settings_window_counter = 0
    settings_window = None
    default_city_entry = None
    default_user_entry = None
    add_location_entry = None
    cities_listbox = None
    temperature_units_radio_var = None
    sf = SettingFile()
    root = None

    def __init__(self):
        settings_window_counter = 0


    def save_user_settings(self):
        default_city = self.default_city_entry.get()
        user_city = self.user_city_entry.get()
        if self.temperature_units_radio_var.get() == 2:
            temperature_units = self.sf.FAHRENHEIT
        else:
            temperature_units = self.sf.CELSIUS

        self.sf.save_settings(default_city, user_city, temperature_units)
        self.quit_settings()

    def add_locations(self):
        locations = str(self.add_location_entry.get())
        locations_list = locations.split(",")
        for location in locations_list:
            location = location.lstrip()
            if location not in self.sf.common_cities:
                self.sf.common_cities.append(location)
                self.cities_listbox.insert(tk.END, location)
        self.add_location_entry.delete(0, tk.END)

    def on_window_close(self):
        self.settings_window_counter = 0

    def quit_settings(self):
        self.settings_window_counter = 0
        self.settings_window.destroy()

    def display_setting_window(self, root, Setting_File):
        self.root = root
        self.sf = Setting_File
        self.settings_window = tk.Toplevel(root)
        self.settings_window.title("User settings")

        default_city_label = tk.Label(self.settings_window, text="Default city: ", anchor=tk.W)
        default_city_label.pack(side=tk.TOP, padx=10, pady=10)
        self.default_city_entry = tk.Entry(self.settings_window)
        self.default_city_entry.insert(0, self.sf.file_settings.get(self.sf.DEFAULT_CITY, ""))
        self.default_city_entry.pack(side=tk.TOP, padx=10, pady=10)
        user_city_label = tk.Label(self.settings_window, text="User city: ", anchor=tk.W)
        user_city_label.pack(side=tk.TOP, padx=10, pady=10)
        self.user_city_entry = tk.Entry(self.settings_window)
        self.user_city_entry.insert(0, self.sf.file_settings.get(self.sf.USER_CITY, ""))
        self.user_city_entry.pack(side=tk.TOP, padx=10, pady=10)

        temperature_units_label = tk.Label(self.settings_window, text="Default temperature units: ", anchor=tk.W)
        temperature_units_label.pack(side=tk.TOP, padx=10, pady=10)
        if self.sf.default_temperature_units == self.sf.FAHRENHEIT:
            self.temperature_units_radio_var = tk.IntVar(value=2)
        else:
            self.temperature_units_radio_var = tk.IntVar(value=1)
        temperature_units_radio_cel = tk.Radiobutton(self.settings_window, text=self.sf.CELSIUS,
                                                     variable=self.temperature_units_radio_var, value=1)
        temperature_units_radio_cel.pack(side=tk.TOP)
        temperature_units_radio_fah = tk.Radiobutton(self.settings_window, text=self.sf.FAHRENHEIT,
                                                     variable=self.temperature_units_radio_var, value=2)
        temperature_units_radio_fah.pack(side=tk.TOP)

        common_cities_label = tk.Label(self.settings_window, text="Common cities: ", anchor=tk.W)
        common_cities_label.pack(side=tk.TOP, padx=10, pady=10)
        self.cities_listbox = tk.Listbox(self.settings_window, selectmode=tk.MULTIPLE)
        self.cities_listbox.pack()
        for city in self.sf.common_cities:
            self.cities_listbox.insert(tk.END, city)

        add_location_label = tk.Label(self.settings_window, text="Add locations to list:", anchor=tk.W)
        add_location_label.pack(side=tk.TOP, padx=10, pady=10)
        self.add_location_entry = tk.Entry(self.settings_window, width = 40)
        self.add_location_entry.pack(side=tk.TOP, padx=10, pady=10)
        add_location_example_label = tk.Label(self.settings_window, text="For example: Tel aviv,London, New york", anchor=tk.W)
        add_location_example_label.pack(side=tk.TOP, padx=10, pady=10)
        add_location_btn = tk.Button(self.settings_window, text="Add", command=self.add_locations)
        add_location_btn.pack(side=tk.TOP, padx=10, pady=10)

        save_btn = tk.Button(self.settings_window, text="Apply", command=self.save_user_settings)
        save_btn.pack(side=tk.TOP, padx=10, pady=10)

        self.settings_window.bind("<Destroy>", lambda e: self.on_window_close())
        self.settings_window.geometry("300x700")
        self.settings_window.mainloop()



