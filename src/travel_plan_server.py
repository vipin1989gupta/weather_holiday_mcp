from mcp.server.fastmcp import FastMCP

import requests
import json


# Create MCP Server
mcp = FastMCP("holiday-planning", "holiday planning Data Server")

# Weather API configuration (assuming your weather server is running locally)
WEATHER_API_BASE = "http://api.openweathermap.org/data/2.5"
API_KEY = "key"

# Temperature thresholds (in Celsius)
TOO_HOT_THRESHOLD = 35
TOO_COLD_THRESHOLD = 5


@mcp.tool()
def decide_holiday_as_per_weather(city: str) -> str:
    """Fetches weather for city planning for holidays

    Args:
        city (str): Name of the city

    Returns:
        str: Weather-based holiday planning for the city
    """
    try:
        print("Fetching weather for holiday planning in city:", city)
        
        # Fetch weather data from OpenWeatherMap API
        url = (f"{WEATHER_API_BASE}/weather?q={city}&appid={API_KEY}"
               f"&units=metric")
        response = requests.get(url)
        data = response.json()
        
        if data.get("cod") != 200:
            error_msg = data.get('message', 'Unknown error')
            return (f"Error: Could not fetch weather data for {city}. "
                    f"{error_msg}")
        
        # Extract weather information
        main_data = data["main"]
        weather_desc = data["weather"][0]["description"]
        temperature = main_data["temp"]
        humidity = main_data["humidity"]
        feels_like = main_data["feels_like"]
        
        # Make travel recommendation based on temperature
        travel_recommendation = make_travel_recommendation(
            temperature, feels_like, weather_desc)
        
        return f"""Holiday Planning Report for {city}:
🌡️ Temperature: {temperature}°C (feels like {feels_like}°C)
🌤️ Weather: {weather_desc.title()}
💧 Humidity: {humidity}%

🧳 Travel Recommendation: {travel_recommendation}"""
        
    except Exception as e:
        return f"Error fetching holiday planning data: {str(e)}"


def make_travel_recommendation(temp: float, feels_like: float,
                               weather: str) -> str:
    """Generate travel recommendation based on weather conditions"""
    
    # Use feels_like temperature for more accurate assessment
    effective_temp = feels_like
    
    if effective_temp > TOO_HOT_THRESHOLD:
        return (f"🔥 TOO HOT! Don't travel - it's {effective_temp}°C "
                f"(feels like). Consider postponing your trip or choose "
                f"an air-conditioned destination.")
    
    elif effective_temp < TOO_COLD_THRESHOLD:
        return (f"🥶 TOO COLD! Don't travel - it's {effective_temp}°C "
                f"(feels like). Pack heavy winter clothes or consider "
                f"a warmer destination.")
    
    elif 15 <= effective_temp <= 25:
        return (f"✅ PERFECT! Ideal weather for travel at {effective_temp}°C. "
                f"Great time to visit!")
    
    elif 25 < effective_temp <= 30:
        return (f"🌞 WARM but manageable at {effective_temp}°C. "
                f"Pack light clothes and stay hydrated.")
    
    elif 10 <= effective_temp < 15:
        return (f"🧥 COOL weather at {effective_temp}°C. "
                f"Pack layers and a light jacket.")
    
    elif 30 < effective_temp <= 35:
        return (f"🔥 HOT at {effective_temp}°C. Pack light, stay in shade, "
                f"and drink lots of water. Consider indoor activities.")
    
    elif 5 <= effective_temp < 10:
        return (f"❄️ COLD at {effective_temp}°C. Pack warm clothes "
                f"and consider indoor attractions.")
    
    else:
        return (f"Weather at {effective_temp}°C. Check local conditions "
                f"and pack accordingly.")


# Start the MCP server
if __name__ == "__main__":
    print("Starting travel Planning Server...")
    mcp.run()
