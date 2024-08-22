import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import time
import webbrowser
from datetime import datetime

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "69ee695048a7e540ac816a5d0f9d7f18"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    # Parse the response JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    feels_like = weather['main']['feels_like'] - 273.15
    min_temp = weather['main']['temp_min'] - 273.15
    max_temp = weather['main']['temp_max'] - 273.15
    humidity = weather['main']['humidity']
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']
    wind_speed = weather['wind']['speed']
    precipitation = weather.get('rain', {}).get('1h', 0)
    is_daytime = icon_id[-1] == 'd'
    
    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, feels_like, min_temp, max_temp, humidity, description, city, country, wind_speed, precipitation, is_daytime)

def open_url(event):
    webbrowser.open_new("https://www.google.co.in/")

# Function to update the time and day/night status
def update_time_and_status():
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    current_date = now.strftime("%B %d, %Y")
    time_label.configure(text=current_time)
    date_label.configure(text=current_date)
    root.after(1000, update_time_and_status)

# Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    
    # If the city is found, unpack the weather information
    (icon_url, temperature, feels_like, min_temp, max_temp, humidity, description, city, country, wind_speed, precipitation, is_daytime) = result
    
    # Update location label
    location_label.configure(text=f"{city}, {country}")
    
    # Update the weather icon
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    
    # Update temperature and other weather details
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C", font="Helvetica 24 bold", foreground="blue")
    feels_like_label.configure(text=f"Feels Like: {feels_like:.2f}°C")
    min_max_label.configure(text=f"Min: {min_temp:.2f}°C | Max: {max_temp:.2f}°C")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    description_label.configure(text=f"Description: {description.capitalize()}")
    wind_speed_label.configure(text=f"Wind Speed: {wind_speed} m/s")
    precipitation_label.configure(text=f"Precipitation: {precipitation} mm")
    day_night_label.configure(text="Daytime" if is_daytime else "Nighttime")

def celsius_to_fahrenheit():
    temperature_text = temperature_label.cget("text")
    feels_like_text = feels_like_label.cget("text")
    min_max_text = min_max_label.cget("text")

    if "°C" in temperature_text:
        # Convert temperature
        celsius = float(temperature_text.split()[1][:-2])
        fahrenheit = (celsius * 9/5) + 32
        temperature_label.configure(text=f"Temperature: {fahrenheit:.2f}°F", font="Helvetica 24 bold", foreground="red")
        
        # Convert "Feels Like" temperature
        celsius_feels_like = float(feels_like_text.split()[2][:-2])
        fahrenheit_feels_like = (celsius_feels_like * 9/5) + 32
        feels_like_label.configure(text=f"Feels Like: {fahrenheit_feels_like:.2f}°F")
        
        # Convert Min and Max temperature
        celsius_min, celsius_max = [float(x.split()[1][:-2]) for x in min_max_text.split("|")]
        fahrenheit_min = (celsius_min * 9/5) + 32
        fahrenheit_max = (celsius_max * 9/5) + 32
        min_max_label.configure(text=f"Min: {fahrenheit_min:.2f}°F | Max: {fahrenheit_max:.2f}°F")

# Create the main application window
root = ttkbootstrap.Window(themename="cosmo")
root.title("Weather Application")
root.geometry("414x736+0+0")  # Position the window at the top-left corner

# Day/Night and Date
day_night_label = tk.Label(root, font="Helvetica, 16", anchor="w")
day_night_label.place(x=10, y=10)

date_label = tk.Label(root, font="Helvetica, 16", anchor="w")
date_label.place(x=10, y=10)

# Current Time
time_label = tk.Label(root, font="Helvetica, 16", anchor="e")
time_label.place(x=1750, y=10)

# Centered "Weather Forecast" Label
title_label = tk.Label(root, text="Weather Forecast", font="Helvetica, 24 bold", foreground="red")
title_label.pack(pady=(10, 20))

# Label for entering city name
city_name_label = tk.Label(root, text="Enter city name ", font="Helvetica, 18")
city_name_label.pack()

# Entry widget -> to enter the city name with icons
city_frame = tk.Frame(root)
city_frame.pack(pady=10)

# Load location and search icons
location_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Shreedhar\Downloads\location.png").resize((50, 50)))
search_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Shreedhar\Downloads\search2.png").resize((45, 45)))

location_label = tk.Label(city_frame, image=location_icon)
location_label.pack(side="left", padx=(0, 5))

city_entry = ttkbootstrap.Entry(city_frame, font="Helvetica, 18")
city_entry.pack(side="left", fill="x", expand=True)

search_button = tk.Button(city_frame, image=search_icon, command=search, borderwidth=1)
search_button.pack(side="right", padx=(5, 0))

convert_button = ttkbootstrap.Button(root, text="Convert to Fahrenheit", command=celsius_to_fahrenheit, bootstyle="info")
convert_button.pack(pady=30)

# Label widget -> to show the city/country name
location_label = tk.Label(root, font="Helvetica, 25", foreground="dark orange")
location_label.pack(pady=20)

# Label widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget -> to show the temperature
temperature_label = tk.Label(root, font="Helvetica, 24 bold", foreground="blue")
temperature_label.pack(pady=(10, 5))

# Label widget -> to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

# Label widget -> to show "Feels Like" temperature
feels_like_label = tk.Label(root, font="Helvetica, 20")
feels_like_label.pack()

# Label widget -> to show min and max temperature
min_max_label = tk.Label(root, font="Helvetica, 20")
min_max_label.pack()

# Label widget -> to show humidity
humidity_label = tk.Label(root, font="Helvetica, 20")
humidity_label.pack()

# Label widget to show the wind speed
wind_speed_label = tk.Label(root, font="Helvetica, 20")
wind_speed_label.pack()

# Label widget to show precipitation
precipitation_label = tk.Label(root, font="Helvetica, 20")
precipitation_label.pack()

# Create a label with your name
label=tk.Label(text="Developed by")
label.place(x=1510, y=780)
font_color = "#228B22"
label = tk.Label(root, text="Shreedhar Kumathalli", fg=font_color, cursor="hand2", font="Helvetica, 16 bold")
label.place(x=1510, y=810)

# Bind the label to the click event
label.bind("<Button-1>", open_url)

# Start updating time and day/night status
update_time_and_status()

# Run the Tkinter event loop
root.mainloop()
