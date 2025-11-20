# Smart Heater Automation

Automatically control your heater smart plugs based on outdoor temperature using OpenWeatherMap API.

## Features

- Monitors outdoor temperature via OpenWeatherMap
- Automatically turns heaters ON when temperature drops below 4°C
- Automatically turns heaters OFF when temperature rises above 5°C
- Supports multiple smart plug types:
  - TP-Link Kasa
  - Tuya/SmartLife
  - Google Home devices (native devices)
- Runs continuously in the background
- Logs all actions to file and console

## Prerequisites

- Python 3.7 or higher
- Windows PC (always-on recommended)
- OpenWeatherMap API key (free)
- Smart plugs connected to your network

## Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

### Step 2: Get OpenWeatherMap API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### Step 3: Install Dependencies

Open Command Prompt in the `heater-automation` folder and run:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Devices

1. Copy `config.example.json` to `config.json`:
   ```bash
   copy config.example.json config.json
   ```

2. Edit `config.json` with your settings:

```json
{
  "openweather_api_key": "your_api_key_here",
  "location": "YourCity,CountryCode",
  "temp_threshold_low": 4,
  "temp_threshold_high": 5,
  "check_interval": 300,

  "kasa_devices": [
    "Living Room Heater",
    "Bedroom Heater"
  ],

  "tuya_devices": [
    {
      "name": "Office Heater",
      "device_id": "your_device_id",
      "ip_address": "192.168.1.100",
      "local_key": "your_local_key",
      "version": 3.3
    }
  ]
}
```

## Configuration Guide

### For TP-Link Kasa Devices

Simply add the device name (as shown in the Kasa app) to the `kasa_devices` array:

```json
"kasa_devices": [
  "Living Room Heater",
  "Bedroom Heater"
]
```

The script will automatically discover these devices on your network.

### For Tuya/SmartLife Devices

You'll need to get device credentials using the Tuya IoT platform:

1. **Get Device Information:**
   - Install the `tinytuya` wizard:
     ```bash
     python -m tinytuya wizard
     ```
   - Follow the prompts to scan your network and get device IDs and local keys

2. **Add to config.json:**
   ```json
   "tuya_devices": [
     {
       "name": "Office Heater",
       "device_id": "eb123456789abcdef",
       "ip_address": "192.168.1.100",
       "local_key": "abc123def456",
       "version": 3.3
     }
   ]
   ```

### Configuration Options

- `openweather_api_key`: Your OpenWeatherMap API key
- `location`: City name and country code (e.g., "London,UK")
- `temp_threshold_low`: Turn heaters ON when temperature drops below this (default: 4°C)
- `temp_threshold_high`: Turn heaters OFF when temperature rises above this (default: 5°C)
- `check_interval`: How often to check temperature in seconds (default: 300 = 5 minutes)

## Running the Script

### Manual Run

Open Command Prompt in the `heater-automation` folder and run:

```bash
python main.py
```

You should see output like:
```
2025-01-20 10:00:00 - INFO - === Heater Automation Started ===
2025-01-20 10:00:00 - INFO - Location: London,UK
2025-01-20 10:00:00 - INFO - Temperature threshold: Below 4°C = ON, Above 5°C = OFF
2025-01-20 10:00:00 - INFO - Current temperature: 6.5°C
2025-01-20 10:00:00 - INFO - Temperature OK - Heaters OFF
```

Press `Ctrl+C` to stop the script.

### Run on Startup (Windows)

To make the script run automatically when your PC starts:

1. **Create a batch file** (`start_heater_automation.bat`):
   ```batch
   @echo off
   cd /d "C:\path\to\heater-automation"
   python main.py
   ```

2. **Add to Windows Startup:**
   - Press `Win+R`, type `shell:startup`, press Enter
   - Create a shortcut to your batch file in this folder

3. **Or use Task Scheduler** (recommended):
   - Open Task Scheduler
   - Create Basic Task
   - Trigger: "When the computer starts"
   - Action: "Start a program"
   - Program: `python`
   - Arguments: `C:\path\to\heater-automation\main.py`
   - Start in: `C:\path\to\heater-automation`

### Run as Windows Service

For a more robust solution, you can install it as a Windows service using NSSM:

1. Download [NSSM](https://nssm.cc/download)
2. Extract and open Command Prompt as Administrator
3. Navigate to NSSM folder and run:
   ```bash
   nssm install HeaterAutomation
   ```
4. In the GUI:
   - Path: `C:\Python3X\python.exe`
   - Startup directory: `C:\path\to\heater-automation`
   - Arguments: `main.py`
5. Click "Install service"
6. Start the service:
   ```bash
   nssm start HeaterAutomation
   ```

## Monitoring

### Check Logs

The script creates a log file `heater_automation.log` in the same folder. You can monitor it to see:
- Temperature readings
- When heaters turn on/off
- Any errors

### Test the System

1. **Test manually first:**
   ```bash
   python main.py
   ```
   Watch the console output to verify it's working

2. **Check device discovery:**
   - The script will log which devices it found
   - If devices aren't found, check your config

3. **Test temperature threshold:**
   - Temporarily change `temp_threshold_low` to a higher value (like 20°C)
   - Run the script and verify it turns on the heaters

## Troubleshooting

### "Cannot find devices"
- Ensure devices are on the same network as your PC
- Check device names match exactly (case-insensitive)
- For Tuya devices, verify device_id and local_key are correct

### "API Key Invalid"
- Verify your OpenWeatherMap API key is correct
- Make sure you've activated the API key (can take a few minutes)

### "Devices won't turn on/off"
- Check if you can control them manually via their apps
- Ensure devices have local control enabled
- Some devices need to be in "LAN control mode"

### Script Crashes
- Check `heater_automation.log` for error details
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Safety Notes

- Always ensure heaters have proper safety features (overheat protection, tip-over switch)
- Don't leave heaters unattended for extended periods
- Test the automation thoroughly before relying on it
- Consider adding a maximum runtime limit for safety
- Keep heaters away from flammable materials

## License

This is free software provided as-is. Use at your own risk.
