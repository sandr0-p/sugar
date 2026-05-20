from Sugar import Sugar

sugar = Sugar(
    wifi_ssid="WIFI-NAME",
    wifi_password="WIFI-PASSWORD",
    dexcom_username="DECOM-USERNAME",
    dexcom_password="DEXCOM-PASSWORD",
)

sugar.display_reading()
sugar.start_reading(interval=60000)  # Start reading every 60 seconds

while True:
    pass