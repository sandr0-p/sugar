from lib.Wifi import Wifi
from lib.Dexcom import Dexcom
from lib.RGB1602 import RGB1602
from lib.Reading import Reading
import machine
import _thread
import time


class Sugar:
    def __init__(self, wifi_ssid: str, wifi_password: str, dexcom_username: str, dexcom_password: str):
        self._wifi = self._startWifi(wifi_ssid, wifi_password)
        self._dexcom = self._start_dexcom(dexcom_username, dexcom_password)
        self._lcd = self._start_lcd()
        self._register_sound()
        self._reading = None
        self._lastReading = None
        self._silence_until = time.time()

    def _startWifi(self, ssid, password) -> Wifi:
        print("Connecting to WiFi...")
        wifi = Wifi(ssid, password)
        wifi.connect()
        return wifi

    def _start_dexcom(self, username: str, password: str) -> Dexcom:
        print("Connecting to Dexcom...")
        return Dexcom(username, password, self._wifi)

    def _start_lcd(self) -> RGB1602:
        print("Initializing LCD...")
        lcd = RGB1602(16, 2)
        lcd.clear()
        self._register_custom_characters(lcd)
        return lcd

    def _register_custom_characters(self, lcd: RGB1602) -> None:
        print("Registering custom characters...")
        cc0 = [0x4, 0xE, 0x1F, 0x15, 0x4, 0x4, 0x0, 0x4]  # Double Up
        cc1 = [0x0, 0x4, 0xE, 0x1F, 0x15, 0x4, 0x4, 0x0]  # Single Up
        cc2 = [0x0, 0x7, 0x3, 0x5, 0x8, 0x10, 0x0, 0x0]  # FourtyFive Up
        cc3 = [0x0, 0xC, 0x6, 0x1F, 0x6, 0xC, 0x0, 0x0]  # Flat
        cc4 = [0x0, 0x10, 0x8, 0x5, 0x3, 0x7, 0x0, 0x0]  # FourtyFive Down
        cc5 = [0x0, 0x4, 0x4, 0x15, 0x1F, 0xE, 0x4, 0x0]  # Single Down
        cc6 = [0x4, 0x0, 0x4, 0x4, 0x15, 0x1F, 0xE, 0x4]  # Double Down
        cc = [cc0, cc1, cc2, cc3, cc4, cc5, cc6]

        for i in range(7):
            lcd.command(0x40 + (i * 8))  # Set CGRAM address
            for j in range(8):
                lcd.write(cc[i][j])  # Write custom character data

    def _register_sound(self):
        print("Registering sound...")
        self._buzzer = machine.Pin(15, machine.Pin.OUT)
        self._buzzer.value(0)
        self._button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
        _thread.start_new_thread(self._silence_alarm, ())

    def start_reading(self, interval: int) -> None:
        print("Starting reading...")
        timer = machine.Timer(-1)
        timer.init(period=interval, mode=machine.Timer.PERIODIC, callback=self._display_reading)

    def _display_reading(self, timer: machine.Timer) -> None:
        self.display_reading()

    def display_reading(self) -> None:
        print("Displaying reading...")
        self._lastReading = self._reading
        self._reading = self._dexcom.get_latest_reading()
        self._lcd.clear()
        self._lcd.setCursor(0, 0)
        value = round(self._reading[0].Value * 0.0555, 1)  # Convert mg/dL to mmol/L

        self._sound_alarm(value)  # Sound alarm if necessary

        trend_arrow = self.get_trend_arrow(self._reading[0].Trend)
        self._lcd.write(trend_arrow)  # Write the custom character for the trend
        self._lcd.printout(f" {value} mmol/L")  # Print the converted value
        if self._lastReading is not None:
            self._lcd.setCursor(0, 1)
            lastTrend_arrow = self.get_trend_arrow(self._lastReading[0].Trend)
            self._lcd.write(lastTrend_arrow)  # Write the custom character for the last trend
            self._lcd.printout(f" {round(self._lastReading[0].Value * 0.0555, 1)} mmol/L")

    def get_trend_arrow(self, trend: str) -> int:
        print(f"Getting trend arrow for: {trend}")
        trend_map = {
            "DoubleUp": 0x00,
            "SingleUp": 0x01,
            "FortyFiveUp": 0x02,
            "Flat": 0x03,
            "FortyFiveDown": 0x04,
            "SingleDown": 0x05,
            "DoubleDown": 0x06,
        }
        return trend_map.get(trend, -1)  # Return -1 if trend is not found

    def _sound_alarm(self, value: int) -> None:
        print(f"Sounding alarm for value: {value}") 
        if time.time() <= self._silence_until:
            print("... but it is silenced.")
            return  # Do not sound the alarm, still silenced
        if value > 4.5 and value < 11:
            print("... but value is in normal range.")
            return  # Do not sound the alarm, value is in normal range
        self._buzzer.value(1)

    def _silence_alarm(self) -> None:
        print("Starting alarm silence thread...")
        while True:
            if self._buzzer.value() == 1 and self._button.value() == 1:
                print("Silencing alarm...")
                self._buzzer.value(0)
                self._silence_until = time.time() + 1200  # Silence for 20 minutes
                time.sleep_ms(100)  # Sleep for 100 milliseconds to avoid busy waiting
            time.sleep_ms(100)  # Sleep for 100 milliseconds to avoid busy waiting
