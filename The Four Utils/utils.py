import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES
from currency_converter import CurrencyConverter
from forex_python.converter import get_symbol
from datetime import datetime
from pytz import timezone, all_timezones, UTC
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pycountry
import requests

# Function to simulate translation using googletrans
def translate_text():
    text = text_input.get()
    target_lang = language_dropdown.get()
    translator = Translator()    
    translated = translator.translate(text, src='en', dest=target_lang.lower())
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, translated.text)

# Function to simulate currency conversion (using a placeholder value)    
def convert_currency():
    cur_from =  currency_from.get().upper()
    cur_to =  currency_to.get().upper()
    c = CurrencyConverter()
    cur_conv = c.convert(currency_amount.get(), cur_from, cur_to)
    # print(c.currencies)
    cur_from =  currency_from.get().upper()
    currency_output_text = f"{currency_amount.get()}{get_symbol(cur_from)} {cur_from} = {cur_conv:.3f}{get_symbol(cur_to)} {cur_to}"
    output_currency.delete(1.0, tk.END)
    output_currency.insert(tk.END, currency_output_text)

# Function to simulate time conversion between timezones
def update_time():
    time_input_val = time_input.get()
    from_tz = timezone_from.get()
    to_tz = timezone_to.get()

    # Convert the input time to a datetime object
    # Assume the input time is in UTC or GMT for conversion
    from_zone = timezone(from_tz)
    to_zone = timezone(to_tz)

    # Parse the input time string to a datetime object
    local_time = datetime.strptime(time_input_val, "%H:%M")

    # Localize the time as UTC (use `UTC` directly instead of any local time zone)
    utc_time = UTC.localize(local_time)

    # Convert UTC time to the destination timezone
    converted_time = utc_time.astimezone(to_zone)

    # Update the output with the converted time
    output_time.delete(1.0, tk.END)
    output_time.insert(tk.END, f"When time in {from_tz} is {time_input_val}-\n Time in {to_tz} is {converted_time.strftime('%H:%M')}")

# # Function to get the capital using REST Countries API
def get_capital(country_name):
    # Send a request to the REST Countries API
    url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Extract the capital from the response (may return a list)
        return data[0].get("capital", "Capital not found")
    else:
        return "Capital not found"

# Function to calculate the distance between two cities
def calc_distance():
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    cap1 = get_capital(distance_from.get())[0]
    cap2 = get_capital(distance_to.get())[0]
    coords_1 = geolocator.geocode(cap1)
    coords_2 = geolocator.geocode(cap2)
    # print(distance_from.get(), distance_to.get(), cap1, cap2, (coords_1.latitude, coords_1.longitude),(coords_2.latitude, coords_2.longitude))
    if coords_1 and coords_2:
        if distance_units.get() == "KM":
            distance = geodesic((coords_1.latitude, coords_1.longitude),(coords_2.latitude, coords_2.longitude)).km
            u = "km"
        else:
            distance = geodesic((coords_1.latitude, coords_1.longitude),(coords_2.latitude, coords_2.longitude)).miles
            u= "miles"
        d_message = f"Distance from {cap1}, {distance_from.get()} to {cap2}, {distance_to.get()} is:\n {distance} {u}"
    else:
        d_message = "One or both cities not found."
    
    output_distance.delete(1.0, tk.END)
    output_distance.insert(tk.END, d_message)

#--------------------------------------------------------
# Create the main window
window = tk.Tk()
window.title("Utilities")

# Create a Frame for each of the sections with different background colors
frame_top_left = tk.Frame(window, padx=10, pady=10, relief="solid", borderwidth=1, bg="#f2f2f2")
frame_top_left.grid(row=0, column=0, sticky="nsew")

frame_top_right = tk.Frame(window, padx=10, pady=10, relief="solid", borderwidth=1, bg="#e0f7fa")
frame_top_right.grid(row=0, column=1, sticky="nsew")

frame_bottom_left = tk.Frame(window, padx=10, pady=10, relief="solid", borderwidth=1, bg="#ffe0b2")
frame_bottom_left.grid(row=1, column=0, sticky="nsew")

frame_bottom_right = tk.Frame(window, padx=10, pady=10, relief="solid", borderwidth=1, bg="#c8e6c9")
frame_bottom_right.grid(row=1, column=1, sticky="nsew")

# Set grid weights so all sections expand properly
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# ------------------- TOP LEFT: Translate Section -------------------
# Translate title
label_translate = tk.Label(frame_top_left, text="Translate from English", font=("Arial", 14, "bold"), bg="#f2f2f2")
label_translate.grid(row=0, column=0, columnspan=4, pady=5)

# Input text
label_text_in = tk.Label(frame_top_left, text="Insert Text:", bg="#f2f2f2")
label_text_in.grid(row=1, column=0, pady=5)
text_input = tk.Entry(frame_top_left, width=30)
text_input.grid(row=1, column=1, pady=5)

# Dropdown selection for languages
label_lang = tk.Label(frame_top_left, text="Select Language:", bg="#f2f2f2")
label_lang.grid(row=2, column=0, pady=5)
languages = [l for l in LANGUAGES.values()]
language_dropdown = ttk.Combobox(frame_top_left, values=languages)
language_dropdown.grid(row=2, column=1, pady=5)
language_dropdown.set("Hebrew")

# Translate button
translate_button = tk.Button(frame_top_left, text="Translate", command=translate_text)
translate_button.grid(row=3, column=1, pady=5)

# Output textbox
output_text = tk.Text(frame_top_left, height=5, width=50)
output_text.grid(row=4, column=0, columnspan=4, pady=5)

# ------------------- TOP RIGHT: Currency Section -------------------
# Currency title
label_currency = tk.Label(frame_top_right, text="Currency", font=("Arial", 14, "bold"), bg="#e0f7fa")
label_currency.grid(row=0, column=0, columnspan=4, pady=5)

# Amount input
label_amount = tk.Label(frame_top_right, text="Insert Amount:", bg="#e0f7fa")
label_amount.grid(row=1, column=0, pady=5)
currency_amount = tk.Entry(frame_top_right, width=10)
currency_amount.grid(row=1, column=1, pady=5)

supported_currencies = [c for c in CurrencyConverter().currencies]
# From currency dropdown
currency_from = ttk.Combobox(frame_top_right, values=supported_currencies)
currency_from.grid(row=2, column=0, pady=5)
currency_from.set("ILS")

# Left-to-right arrow between currency_from and currency_to
arrow_label = tk.Label(frame_top_right, text="→", font=("Arial", 16), bg="#e0f7fa", width=10)
arrow_label.grid(row=2, column=1, pady=5)

# To currency dropdown
currency_to = ttk.Combobox(frame_top_right, values=supported_currencies)
currency_to.grid(row=2, column=2, pady=5)
currency_to.set("USD")
# Convert button
convert_button = tk.Button(frame_top_right, text="Convert", command=convert_currency)
convert_button.grid(row=3, column=1, pady=5)

# Output textbox
output_currency = tk.Text(frame_top_right, height=5, width=30)
output_currency.grid(row=4, column=0, columnspan=4, pady=5)

# ------------------- BOTTOM LEFT: Time Section -------------------
# Time title
label_time = tk.Label(frame_bottom_left, text="Time", font=("Arial", 14, "bold"), bg="#ffe0b2")
label_time.grid(row=0, column=0, columnspan=4, pady=5)

# Time input
label_time_in = tk.Label(frame_bottom_left, text="Insert Time: ", bg="#ffe0b2")
label_time_in.grid(row=1, column=0, pady=5)
time_input = tk.Entry(frame_bottom_left, width=15)
time_input.grid(row=1, column=1, pady=5)

# From timezone dropdown
timezones = [t for t in all_timezones]
timezone_from = ttk.Combobox(frame_bottom_left, values=timezones)
timezone_from.grid(row=2, column=0, pady=5)
timezone_from.set("Israel")

# Left-to-right arrow between from and to
arrow_label_t = tk.Label(frame_bottom_left, text="→", font=("Arial", 16), bg="#ffe0b2")
arrow_label_t.grid(row=2, column=1, pady=5)

# To timezone dropdown
timezone_to = ttk.Combobox(frame_bottom_left, values=timezones)
timezone_to.grid(row=2, column=2, pady=5)
timezone_to.set("US/Hawaii")

# Update button
update_button = tk.Button(frame_bottom_left, text="Update", command=update_time)
update_button.grid(row=3, column=1, pady=5)

# Output textbox
output_time = tk.Text(frame_bottom_left, height=5, width=30)
output_time.grid(row=4, column=0, columnspan=4, pady=5)

# ------------------- BOTTOM RIGHT: Distances Section -------------------
# Distance title
label_distance = tk.Label(frame_bottom_right, text="Country Distances", font=("Arial", 14, "bold"), bg="#c8e6c9")
label_distance.grid(row=0, column=0, columnspan=4, pady=5)

# From country-capital dropdown
countries = [country.name for country in pycountry.countries]
distance_from = ttk.Combobox(frame_bottom_right, values=countries)
distance_from.grid(row=1, column=0, pady=5)
distance_from.set("Israel")

# Left-to-right arrow between from and to
arrow_label_d = tk.Label(frame_bottom_right, text="→", font=("Arial", 16), bg="#c8e6c9")
arrow_label_d.grid(row=1, column=1, pady=5)

# To country-capital dropdown
distance_to = ttk.Combobox(frame_bottom_right, values=countries)
distance_to.grid(row=1, column=2, pady=5)
distance_to.set("Aruba")
#units
units_d = tk.Label(frame_bottom_right, text="Units:", bg="#c8e6c9", width=10)
units_d.grid(row=2, column=0, pady=5)
distance_units = ttk.Combobox(frame_bottom_right, values=["KM", "Miles"], width=10)
distance_units.grid(row=2, column=1, pady=5)
distance_units.set("KM")
# Calculate distance button
calc_button = tk.Button(frame_bottom_right, text="Calc Distance", command=calc_distance)
calc_button.grid(row=2, column=2, pady=5)

# Output textbox
output_distance = tk.Text(frame_bottom_right, height=5, width=50)
output_distance.grid(row=3, column=0, columnspan=4, pady=5)

# Run the window
window.mainloop()
