import network
import lib.RGB1602 as RGB1602
import time


class Wifi:
    """
    Manages WiFi connectivity using the network module and displays status on an RGB1602 LCD.

    Attributes:
        ssid (str): The SSID of the WiFi network.
        password (str): The password for the WiFi network.
        wlan (network.WLAN): The WLAN interface object.
    """

    def __init__(self, ssid: str, password: str):
        """
        Initializes the Wifi object with network credentials and LCD display.

        Args:
            ssid (str): WiFi network SSID.
            password (str): WiFi network password.
            lcd (RGB1602.RGB1602): LCD display object for status output.
        """
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self):
        """
        Connects to the WiFi network and displays connection status on the LCD.
        If already connected, does nothing. Otherwise, attempts to reconnect and
        updates the LCD with progress messages.
        """
        if not self.wlan.isconnected():
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected():
                time.sleep(1)
