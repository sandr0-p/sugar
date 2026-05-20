# sugar

## Overview
Sugar is a Python-based project designed to monitor and display blood glucose readings using a Dexcom Continuous Glucose Monitoring (CGM) system. It connects to WiFi, retrieves data from Dexcom, and displays the readings on an LCD screen. The system also includes an alarm feature to notify users of abnormal glucose levels.

## Features
- **WiFi Connectivity**: Connects to a WiFi network for data retrieval.
- **Dexcom Integration**: Retrieves real-time glucose readings from the Dexcom CGM system.
- **LCD Display**: Displays current and previous glucose readings along with trend arrows.
- **Custom Characters**: Uses custom characters on the LCD to represent glucose trends.
- **Alarm System**: Sounds an alarm for abnormal glucose levels, with a manual silence option.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sugar.git
   ```
2. Navigate to the project directory:
   ```bash
   cd sugar
   ```
3. Install the required dependencies (if any).

## Usage
1. Open the `main.py` file and configure the following parameters:
   ```python
   sugar = Sugar(
       wifi_ssid="WIFI-NAME",
       wifi_password="WIFI-PASSWORD",
       dexcom_username="DEXCOM-USERNAME",
       dexcom_password="DEXCOM-PASSWORD",
   )
   ```
   Replace `WIFI-NAME`, `WIFI-PASSWORD`, `DEXCOM-USERNAME`, and `DEXCOM-PASSWORD` with your credentials.

2. Run the application:
   ```bash
   python main.py
   ```

## File Structure
- `main.py`: Entry point of the application.
- `Sugar.py`: Contains the `Sugar` class, which manages WiFi, Dexcom, LCD, and alarm functionalities.
- `lib/`: Contains helper modules:
  - `Wifi.py`: Manages WiFi connectivity.
  - `Dexcom.py`: Handles Dexcom API interactions.
  - `RGB1602.py`: Controls the LCD display.
  - `Reading.py`: Processes glucose reading data.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.