import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

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

    url = "http://api.openweathermap.org/data/2.5/weather"

    parameters = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=parameters, timeout=5)
        response.raise_for_status()

        data = response.json()

        return {
            "status": "success",
            "weather": {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "condition": data["weather"][0]["description"],
                "lat": data["coord"]["lat"],
                "lon": data["coord"]["lon"]
            }
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Request timed out"
        }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "No internet connection"
        }

    except requests.exceptions.RequestException:
        return {
            "status": "error",
            "message": "Weather service unavailable"
        }

def get_aqi(lat, lon):

    url = "http://api.openweathermap.org/data/2.5/air_pollution"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {
            "aqi": {
                "aqi": None,
                "category": "Unknown",
                "advisory": "AQI data unavailable"
            }
        }
    except requests.exceptions.ConnectionError:
        return {
            "aqi": {
                "aqi": None,
                "category": "Unknown",
                "advisory": "AQI data unavailable"
            }
        }
    except requests.exceptions.RequestException:
        return {
            "aqi": {
                "aqi": None,
                "category": "Unknown",
                "advisory": "AQI data unavailable"
            }
        }

    if response.status_code == 200:

        data = response.json()

        aqi_value = data["list"][0]["main"]["aqi"]


        return {
            "aqi": {
                "aqi": aqi_value,
                "category": get_aqi_health(aqi_value),
                "advisory": get_aqi_advisory(aqi_value)
            }
        }

    else:
        return {
            "aqi": {
                "aqi": None,
                "category": "Unknown",
                "advisory": "AQI data unavailable"
            }
        }

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
        
def get_aqi_advisory(aqi):
    match aqi:
        case 1:
            return "Air quality is good. Enjoy outdoor activities."
        case 2:
            return "Acceptable air quality. Sensitive individuals may want to consider limiting prolonged outdoor exertion."
        case 3:
            return "Sensitive individuals should reduce outdoor activity."
        case 4:
            return "Avoid outdoor exertion if possible."
        case 5:
            return "Health warning: stay indoors recommended."
        case _:
            return "AQI data unavailable"

def display_weather(record):
    if record["status"] == "not found":
        print(f"Weather data for {record['city']} not found.")
    else:
        weather = record["weather"]
        aqi = record["aqi"]
        city = weather["city"]
        temperature = weather["temperature"]
        humidity = weather["humidity"]
        wind_speed = weather["wind_speed"]
        condition = weather["condition"]
        aqi_value = aqi["aqi"]
        category = aqi["category"]
        advisory = aqi["advisory"]
        print(f"\n Weather in {city}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Condition: {condition}")
        print(f"Air Quality Index: {aqi_value} - {category}")
        print(f"Advisory: {advisory} \n")

def get_weather_with_aqi(city):

    weather_result = get_weather(city)

    if weather_result["status"] != "success":
        return weather_result

    lat = weather_result["weather"]["lat"]
    lon = weather_result["weather"]["lon"]

    aqi_result = get_aqi(lat, lon)

    return {
        "status": "success",
        "weather": weather_result["weather"],
        "aqi": aqi_result["aqi"]
    }

def main():

    history = load_history()
    show_last_saved(history)

    print("\nEnter a city name to view its weather and AQI, 'history' to view search history, or 'exit' to quit\n")
    while True:

        city = input("City: ").strip()

        if city.lower() == "exit":
            print("program ending...")
            break

        elif city.lower() == "history":
            show_history(history)

        else:
            result = get_weather_with_aqi(city)

            if result["status"] == "success":   
                display_weather(result)
                history.append(result)
                history = history[-5:]
                save_history(history)

            else:
                print(f"\nError: {result.get('message', 'Something went wrong')}\n")




main()
