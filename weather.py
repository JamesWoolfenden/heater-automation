"""
Weather monitoring using OpenWeatherMap API
"""

import aiohttp
import logging

logger = logging.getLogger(__name__)


class WeatherMonitor:
    def __init__(self, api_key, location):
        self.api_key = api_key
        self.location = location
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_temperature(self):
        """Get current temperature from OpenWeatherMap"""
        params = {
            'q': self.location,
            'appid': self.api_key,
            'units': 'metric'  # Celsius
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        temperature = data['main']['temp']
                        return round(temperature, 1)
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenWeatherMap API error: {response.status} - {error_text}")
                        raise Exception(f"API returned status {response.status}")
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            raise
