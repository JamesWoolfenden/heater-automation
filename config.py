"""
Configuration management for heater automation
"""

import json
import os
import logging

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            logger.error(f"Configuration file not found: {self.config_file}")
            logger.error("Please create config.json using config.example.json as a template")
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)

            # OpenWeatherMap settings
            self.openweather_api_key = config.get('openweather_api_key', '')
            self.location = config.get('location', '')

            # Temperature thresholds
            self.temp_threshold_low = config.get('temp_threshold_low', 4)
            self.temp_threshold_high = config.get('temp_threshold_high', 5)

            # Check interval (in seconds)
            self.check_interval = config.get('check_interval', 300)

            # Device configurations
            self.kasa_devices = config.get('kasa_devices', [])
            self.tuya_devices = config.get('tuya_devices', [])
            self.google_home_devices = config.get('google_home_devices', [])

            # Validate required fields
            if not self.openweather_api_key:
                raise ValueError("openweather_api_key is required in config.json")
            if not self.location:
                raise ValueError("location is required in config.json")

            logger.info("Configuration loaded successfully")

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
