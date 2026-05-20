from Sugar import Sugar

sugar = Sugar(
    wifi_ssid="PLUSNET-9FF6SJ",
    wifi_password="hd6vkLPbCQL6tn",
    dexcom_username="BiancaJasmina",
    dexcom_password="PMF!uru.nxe_zfu2zhm",
)

sugar.display_reading()
sugar.start_reading(interval=60000)  # Start reading every 60 seconds

while True:
    pass