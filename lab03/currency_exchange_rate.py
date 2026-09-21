import sys
import os
import json
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(
    filename="full.log",
    filemode="a",
    encoding='utf-8',
    format='%(asctime)s\t%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logging.getLogger(__name__)

load_dotenv()

class ApiClient:
    def __init__(self, baseUrl, apiKey) -> None:
        self._baseUrl = str(baseUrl)
        self._apiKey = str(apiKey)
        self._currencies = []

    def saveResponse(self, fromCurr, toCurr, date, content):
        if not os.path.exists("data"):
            os.makedirs("data")
            logging.info("API Client data directory created")

        fileName = f"data/{fromCurr}_{toCurr}_{date}_{datetime.now().timestamp()}.json"

        with open(fileName, "w", encoding="utf-8") as responseFile:
            json.dump(content, responseFile, indent=4)

        logging.info(f"API Client saveResponse('{fileName}') done")
        print(f"Saved to {fileName}")

    def getCurrencies(self):
        logging.info("API Client getCurrencies() issued")

        try:
            response = requests.post(url=self._baseUrl, params={'currencies': ''}, data={"key": self._apiKey})
        except Exception as e:
            print(f"[E] request failed: {e}")
            logging.error(f"API Client getCurrencies() request failed: {e}")
            return False
        logging.info(f"API Client getCurrencies() response received: {response.text}")

        try:
            parsedJson = response.json()
        except Exception as e:
            print(f"[E] bad response: {e}")
            logging.error(f"API Client getCurrencies() bad response: {e}")
            return False

        if parsedJson["error"] != "":
            print(f"[E] {parsedJson['error']}")
            logging.error(f"API Client getCurrencies() error: {parsedJson['error']}")
            return False

        self._currencies = parsedJson["data"]
        logging.info(f"API Client getCurrencies() got: {self._currencies}")
        # print(self._currencies)
        return True

    def getExchange(self, currFrom, currTo, date):
        logging.info(f"API Client getExchange('{currFrom}', '{currTo}', '{date}') issued")

        if currFrom not in self._currencies:
            print(f"[E] unknown currFrom currency: {currFrom}")
            logging.error(f"API Client getExchange() unknown currFrom currency: {currFrom}")
            return

        if currTo not in self._currencies:
            print(f"[E] unknown currTo currency: {currTo}")
            logging.error(f"API Client getExchange() unknown currTo currency: {currTo}")
            return

        params = {
            'from': currFrom,
            'to': currTo,
            'date': date
        }

        logging.info(f"API Client POST {self._baseUrl} params={params} issued")

        try:
            response = requests.post(url=self._baseUrl, params=params, data={"key": self._apiKey})
        except Exception as e:
            print(f"[E] request failed: {e}")
            logging.error(f"API Client getExchange('{currFrom}', '{currTo}', '{date}') request failed: {e}")
            return

        logging.info(f"API Client getExchange('{currFrom}', '{currTo}', '{date}') response received: {response.text}")
        # print(response.text)

        try:
            parsedJson = response.json()
        except Exception as e:
            print(f"[E] bad response: {e}")
            logging.error(f"API Client getExchange() bad response: {e}")
            return

        if parsedJson["error"] != "":
            print(f"[E] {parsedJson['error']}")
            logging.error(f"API Client getExchange() error: {parsedJson['error']}")
            return

        self.saveResponse(currFrom, currTo, date, parsedJson)

def main():
    if len(sys.argv) != 4:
        print(f"[E] usage: python {sys.argv[0]} <from> <to> <date YYYY-MM-DD>")

        logging.error(f"API Client wrong args: {sys.argv}")

        return

    logging.error(f"API Client ran with args: {sys.argv}")
    currFrom = str(sys.argv[1]).upper()
    currTo = str(sys.argv[2]).upper()
    date = str(sys.argv[3])

    baseUrl = os.getenv("BASE_URL") or "http://localhost:8080"
    apiKey = os.getenv("API_KEY") or "EXAMPLE_API_KEY"

    apiClient = ApiClient(baseUrl, apiKey)
    ok = apiClient.getCurrencies()

    if ok == False:
        return

    apiClient.getExchange(currFrom, currTo, date)

main()
