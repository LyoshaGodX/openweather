import math

import json
from pprint import pprint

import requests


def get_weather_data(city, api_key=None):
    if not api_key:
        return None

    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        city_info = weather_data.get("city", {})

        city_name = city_info.get("name", "N/A")

        coordinates = city_info.get("coord", {})
        latitude = coordinates.get("lat", "N/A")
        longitude = coordinates.get("lon", "N/A")

        country_name = city_info.get("country", "N/A")

        weather_info = weather_data.get("list", {})

        feels_like = weather_info[0].get("main", {}).get("feels_like", "N/A")

        timezone = city_info.get("timezone", float("NaN"))/3600
        timezone_sign = "+" if math.copysign(1, timezone) > 0 else ""

        result = json.dumps(
            {
                "name": city_name,
                "coord": {
                    "lon": longitude,
                    "lat": latitude
                },
                "country": country_name,
                "feels_like": feels_like,
                "timezone": "UTC" + timezone_sign + str(int(timezone))
            }
        )

        return result

    else:
        return None

