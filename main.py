"""
Weather App

This application fetches weather information from a user-provided API URL
and displays it in a Tkinter GUI.

Author: MrKaplan
Date: 24/04/2024

"""

import tkinter as tk
from tkinter import messagebox
import requests

def get_weather(api_url):
    """
    Retrieve weather information from the provided API URL.

    Parameters:
    - api_url (str): The API URL to fetch weather data from.

    Returns:
    - dict or None: A dictionary containing weather information if successful,
                    None otherwise.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()

        if "days" in data:
            weather_info = {
                "temperature": data["days"][0]["temp"],
                "description": data["days"][0]["conditions"],
                "humidity": data["days"][0]["humidity"],
                "wind_speed": data["days"][0]["windspeed"]
            }
            return weather_info
        elif "alerts" in data:
            alerts = [alert["description"] for alert in data["alerts"]]
            messagebox.showwarning("Weather Alerts", "\n".join(alerts))
            return None
        else:
            messagebox.showinfo("Information", "No weather data available.")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve weather data: {str(e)}")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        return None

def fetch_weather():
    """
    Fetch weather data when the 'Fetch Weather' button is clicked.
    """
    api_url = api_url_entry.get()

    if api_url == "":
        messagebox.showerror("Error", "Please enter API URL.")
        return

    weather_info = get_weather(api_url)

    if weather_info:
        temperature_label.config(text=f"Temperature: {weather_info['temperature']}°C")
        description_label.config(text=f"Description: {weather_info['description'].capitalize()}")
        humidity_label.config(text=f"Humidity: {weather_info['humidity']}%")
        wind_speed_label.config(text=f"Wind Speed: {weather_info['wind_speed']} m/s")

# Create main window
root = tk.Tk()
root.title("Weather App")

# Create labels and entry fields
api_url_label = tk.Label(root, text="Enter API URL:")
api_url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
api_url_entry = tk.Entry(root, width=50)
api_url_entry.insert(tk.END, "")
api_url_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

fetch_button = tk.Button(root, text="Fetch Weather", command=fetch_weather)
fetch_button.grid(row=1, column=0, columnspan=3, pady=10)

temperature_label = tk.Label(root, text="")
temperature_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

description_label = tk.Label(root, text="")
description_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

humidity_label = tk.Label(root, text="")
humidity_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

wind_speed_label = tk.Label(root, text="")
wind_speed_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

root.mainloop()
