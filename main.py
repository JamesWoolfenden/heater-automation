#!/usr/bin/env python3
"""
Smart Heater Automation Script
Monitors outdoor temperature and controls smart plugs connected to heaters
"""

import asyncio
import logging
from datetime import datetime
import sys
from config import Config
from weather import WeatherMonitor
from devices import DeviceController

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('heater_automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class HeaterAutomation:
    def __init__(self):
        self.config = Config()
        self.weather = WeatherMonitor(self.config.openweather_api_key, self.config.location)
        self.devices = DeviceController(self.config)
        self.heaters_on = False

    async def check_and_control(self):
        """Check temperature and control heaters accordingly"""
        try:
            temperature = await self.weather.get_temperature()
            logger.info(f"Current temperature: {temperature}°C")

            # Temperature threshold: turn on below 4°C, turn off above 5°C (1° hysteresis)
            if temperature < self.config.temp_threshold_low and not self.heaters_on:
                logger.info(f"Temperature below {self.config.temp_threshold_low}°C - Turning ON heaters")
                await self.devices.turn_on_all()
                self.heaters_on = True

            elif temperature > self.config.temp_threshold_high and self.heaters_on:
                logger.info(f"Temperature above {self.config.temp_threshold_high}°C - Turning OFF heaters")
                await self.devices.turn_off_all()
                self.heaters_on = False
            else:
                logger.info(f"Temperature OK - Heaters {'ON' if self.heaters_on else 'OFF'}")

        except Exception as e:
            logger.error(f"Error in check_and_control: {e}")

    async def run(self):
        """Main loop"""
        logger.info("=== Heater Automation Started ===")
        logger.info(f"Location: {self.config.location}")
        logger.info(f"Temperature threshold: Below {self.config.temp_threshold_low}°C = ON, Above {self.config.temp_threshold_high}°C = OFF")
        logger.info(f"Check interval: {self.config.check_interval} seconds")

        # Initialize devices
        await self.devices.initialize()

        while True:
            try:
                await self.check_and_control()
                await asyncio.sleep(self.config.check_interval)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    automation = HeaterAutomation()
    asyncio.run(automation.run())
