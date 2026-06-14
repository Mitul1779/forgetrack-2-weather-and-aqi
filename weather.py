import os
import json

def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r") as file:
                history = json.load(file)
        except json.JSONDecodeError:
            history = []
    else:
        history = []
    return history

def save_history(history):             #only keep last 5
    with open("history.json", "w") as file:
        json.dump(history[-5:], file)

def show_history(history):
    for record in history:
        display_weather(record)

def show_last_saved(history):
    if history:
        display_weather(history[-1])

def get_weather(city):
    pass

def get_aqi(lat, lon):
    pass

def get_aqi_health(aqi):
    match aqi:
        case 1:
            return "Good"
        case 2:
            return "Fair"
        case 3:
            return "Moderate"
        case 4:
            return "Poor"
        case 5:
            return "Very Poor"
        case _:
            return "Unknown"

def display_weather(record):
    pass