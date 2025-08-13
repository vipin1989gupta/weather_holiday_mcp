from mcp.server.fastmcp import FastMCP

import requests
import json

# OpenWeatherMap API Key
API_KEY = "key"
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Create MCP Server
mcp = FastMCP("weather-server", "Weather Data Server")

# function to fetch current weather data


@mcp.tool()
def get_weather(city: str) -> str:
    """Fetches weather for the current city

    Args:
        city (str): _description_

    Returns:
        str: _description_
    """
    try:
        print("Fetching current weather for city:", city)
    #  return f"{city} weather is good"
    #     # Uncomment the following lines to enable actual API calls
        url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"Error: {data.get('message')}"
        main_data = data["main"]
        weather = data["weather"][0]["description"]
        temprature = main_data["temp"]
        humidity = main_data["humidity"]
        return f"The current weather in {city} is {weather} with temprature of {temprature} and humidity {humidity}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


# Start the MCP server
if __name__ == "__main__":
    print("Starting Weather Data Server...")
    mcp.run()
