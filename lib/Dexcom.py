import urequests
import json
from lib.Reading import Reading
from lib.Wifi import Wifi

# wlan.connect("PLUSNET-9FF6SJ", "hd6vkLPbCQL6tn")

# while not wlan.isconnected():
#     print("Waiting for connection...")
#     time.sleep(1)

# print("Connected to WiFi!")

DEXCOM_BASE_URL = "https://shareous1.dexcom.com/ShareWebServices/Services/"
DEXCOM_LOGIN_ENDPOINT: str = "General/LoginPublisherAccountById"
DEXCOM_AUTHENTICATE_ENDPOINT: str = "General/AuthenticatePublisherAccount"
DEXCOM_GLUCOSE_READINGS_ENDPOINT: str = "Publisher/ReadPublisherLatestGlucoseValues"
DEXCOM_HEADERS = {"content-type": "application/json"}

# requestData = json.dumps(
#     {
#         "accountName": "BiancaJasmina",
#         "password": "PMF!uru.nxe_zfu2zhm",
#         "applicationId": "d89443d2-327c-4a6f-89e5-496bbb0317db",
#     }
# )
# requestUrl = DEXCOM_BASE_URL + DEXCOM_AUTHENTICATE_ENDPOINT
# accountId = urequests.post(requestUrl, data=requestData, headers=DEXCOM_HEADERS).text[1:-1]
# print("Authentication response:", accountId)

# requestData = json.dumps(
#     {
#         "accountId": accountId,
#         "password": "PMF!uru.nxe_zfu2zhm",
#         "applicationId": "d89443d2-327c-4a6f-89e5-496bbb0317db",
#     }
# )
# requestUrl = DEXCOM_BASE_URL + DEXCOM_LOGIN_ENDPOINT
# sessionId = urequests.post(requestUrl, data=requestData, headers=DEXCOM_HEADERS).text[1:-1]
# print("Login response:", sessionId)

# requestData = json.dumps({"sessionId": sessionId, "minutes": "10", "maxCount": "1"})
# requestUrl = DEXCOM_BASE_URL + DEXCOM_GLUCOSE_READINGS_ENDPOINT
# glucoseReadings = urequests.post(requestUrl, data=requestData, headers=headerData)
# print("Glucose readings response:", glucoseReadings.json())

# data_list = glucoseReadings.json()
# readings = [Reading.from_dict(item) for item in data_list]

# for reading in readings:
#     mmol_L = round(reading.Value * 0.0555, 1)  # Convert mg/dL to mmol/L
#     print(f"WT: {reading.WT}, ST: {reading.ST}, DT: {reading.DT}, Value: {mmol_L}, Trend: {reading.Trend}")


class Dexcom:
    """
    Handles authentication and data retrieval from the Dexcom Share API.

    Attributes:
        _accountId (str): The Dexcom account ID obtained after authentication.
        _sessionId (str): The session ID for API requests.
        _wlan (network.WLAN): The WLAN interface used for network connectivity.
    """

    def __init__(self, username: str, password: str, wifi: Wifi):
        """
        Initializes the Dexcom object and authenticates with the Dexcom Share API.

        Args:
            username (str): Dexcom account username.
            password (str): Dexcom account password.
            wlan (network.WLAN): WLAN interface for network connectivity.
        """
        self._accountId = self._get_account(username, password)
        self._sessionId = self._get_session(self._accountId)
        self._wlan = wifi.wlan

    def _get_account(self, username: str, password: str) -> str:
        """
        Authenticates the user and retrieves the Dexcom account ID.

        Returns:
            str: The authenticated Dexcom account ID.
        """
        print("Authenticating Dexcom account...")
        requestData = json.dumps(
            {
                "accountName": username,
                "password": password,
                "applicationId": "d89443d2-327c-4a6f-89e5-496bbb0317db",
            }
        )
        requestUrl = DEXCOM_BASE_URL + DEXCOM_AUTHENTICATE_ENDPOINT
        response = urequests.post(requestUrl, data=requestData, headers=DEXCOM_HEADERS)
        return response.text[1:-1]

    def _get_session(self, accountId: str) -> str:
        """
        Logs in to the Dexcom Share API and retrieves a session ID.

        Args:
            accountId (str): The authenticated Dexcom account ID.

        Returns:
            str: The session ID for API requests.
        """
        print("Logging in to Dexcom Share API...")
        requestData = json.dumps(
            {
                "accountId": accountId,
                "password": "PMF!uru.nxe_zfu2zhm",
                "applicationId": "d89443d2-327c-4a6f-89e5-496bbb0317db",
            }
        )
        requestUrl = DEXCOM_BASE_URL + DEXCOM_LOGIN_ENDPOINT
        response = urequests.post(requestUrl, data=requestData, headers=DEXCOM_HEADERS)
        return response.text[1:-1]

    def _get_latest_reading(self, sessionId: str) -> list[Reading]:
        """
        Fetches the latest glucose reading from the Dexcom Share API.

        Args:
            sessionId (str): The session ID for API requests.

        Returns:
            list[Reading]: A list containing the latest Reading object(s).
        """
        print("Fetching latest glucose reading...")
        requestData = json.dumps({"sessionId": sessionId, "minutes": "10", "maxCount": "1"})
        requestUrl = DEXCOM_BASE_URL + DEXCOM_GLUCOSE_READINGS_ENDPOINT
        glucoseReadings = urequests.post(requestUrl, data=requestData, headers=DEXCOM_HEADERS)

        data_list = glucoseReadings.json()
        readings = [Reading.from_dict(item) for item in data_list]

        return readings

    def get_latest_reading(self) -> list[Reading]:
        """
        Retrieves the latest glucose reading using the current session ID.

        Returns:
            list[Reading]: A list containing the latest Reading object(s).
        """
        return self._get_latest_reading(self._sessionId)
