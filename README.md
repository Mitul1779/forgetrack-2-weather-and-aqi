# Weather + AQI CLI Application

A Python command-line project that fetches real-time weather and air quality data using the OpenWeather API. It also stores search history locally and displays formatted results in the terminal.

# Features
-Fetch current weather data for any city  
-Display temperature, humidity, wind speed, and weather condition  
-Fetch Air Quality Index (AQI) with category and advisory  
-Store last 5 searches in a local JSON file  
-Load and display previous search history  

# Setup Instructions
1. Clone the repository
git clone <repository-url>
>> cd <project-folder>

2. Install dependencies
>> pip install requests python-dotenv

3. Create environment file
Create a .env file from the example:
>> cp .env.example .env

4. Add API key
Open the .env file and add your OpenWeather API key:
OPENWEATHER_API_KEY=your_actual_api_key_here

5. Run the program
>> python main.py

# How it works
i. User enters a city name  
ii. Weather data is fetched from OpenWeather API  
iii. Coordinates are used to fetch AQI data  
iv. Combined result is displayed in the terminal  
v. Search is saved in history (maximum 5 entries)  
vi. Previous searches can be viewed using the history command  
