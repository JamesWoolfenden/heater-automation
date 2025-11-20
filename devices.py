"""
Device controller for TP-Link Kasa, Tuya/SmartLife, and Google Home devices
"""

import asyncio
import logging
from kasa import Discover, SmartPlug
from tinytuya import OutletDevice
import json

logger = logging.getLogger(__name__)


class DeviceController:
    def __init__(self, config):
        self.config = config
        self.kasa_devices = []
        self.tuya_devices = []

    async def initialize(self):
        """Initialize and discover all devices"""
        logger.info("Initializing devices...")

        # Initialize TP-Link Kasa devices
        if self.config.kasa_devices:
            await self._init_kasa_devices()

        # Initialize Tuya devices
        if self.config.tuya_devices:
            self._init_tuya_devices()

        logger.info(f"Initialized {len(self.kasa_devices)} Kasa devices and {len(self.tuya_devices)} Tuya devices")

    async def _init_kasa_devices(self):
        """Initialize TP-Link Kasa devices"""
        try:
            for device_name in self.config.kasa_devices:
                logger.info(f"Looking for Kasa device: {device_name}")
                # Discover devices on the network
                devices = await Discover.discover()
                for ip, dev in devices.items():
                    await dev.update()
                    if device_name.lower() in dev.alias.lower():
                        self.kasa_devices.append(dev)
                        logger.info(f"Found Kasa device: {dev.alias} at {ip}")
        except Exception as e:
            logger.error(f"Error initializing Kasa devices: {e}")

    def _init_tuya_devices(self):
        """Initialize Tuya/SmartLife devices"""
        try:
            for device_config in self.config.tuya_devices:
                device = OutletDevice(
                    dev_id=device_config['device_id'],
                    address=device_config['ip_address'],
                    local_key=device_config['local_key'],
                    version=device_config.get('version', 3.3)
                )
                self.tuya_devices.append({
                    'name': device_config['name'],
                    'device': device
                })
                logger.info(f"Initialized Tuya device: {device_config['name']}")
        except Exception as e:
            logger.error(f"Error initializing Tuya devices: {e}")

    async def turn_on_all(self):
        """Turn on all heater devices"""
        logger.info("Turning ON all heater devices...")

        # Turn on Kasa devices
        for device in self.kasa_devices:
            try:
                await device.turn_on()
                logger.info(f"Turned ON: {device.alias}")
            except Exception as e:
                logger.error(f"Error turning on Kasa device {device.alias}: {e}")

        # Turn on Tuya devices
        for item in self.tuya_devices:
            try:
                item['device'].turn_on()
                logger.info(f"Turned ON: {item['name']}")
            except Exception as e:
                logger.error(f"Error turning on Tuya device {item['name']}: {e}")

    async def turn_off_all(self):
        """Turn off all heater devices"""
        logger.info("Turning OFF all heater devices...")

        # Turn off Kasa devices
        for device in self.kasa_devices:
            try:
                await device.turn_off()
                logger.info(f"Turned OFF: {device.alias}")
            except Exception as e:
                logger.error(f"Error turning off Kasa device {device.alias}: {e}")

        # Turn off Tuya devices
        for item in self.tuya_devices:
            try:
                item['device'].turn_off()
                logger.info(f"Turned OFF: {item['name']}")
            except Exception as e:
                logger.error(f"Error turning off Tuya device {item['name']}: {e}")
