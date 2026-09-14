import sys
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class ApiClient:
    def __init__(self, baseUrl, apiKey) -> None:
        self._baseUrl = str(baseUrl)
        self._apiKey = str(apiKey)
        self._currencies = []

    def log(self, msg, level="Debug"):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{time}\t[{level}]\t{msg}\n"

        with open("full.log", "a", encoding="utf-8") as logFile:
            logFile.write(line)

        if level == "Error":
            with open("error.log", "a", encoding="utf-8") as logFile:
                logFile.write(line)

    def saveResponse(self, fromCurr, toCurr, date, content):
        if not os.path.exists("data"):
            os.makedirs("data")
            self.log("API Client data directory created")

        fileName = f"data/{fromCurr}_{toCurr}_{date}_{datetime.now().timestamp()}.json"

        with open(fileName, "w", encoding="utf-8") as responseFile:
            json.dump(content, responseFile, indent=4)

        self.log(f"API Client saveResponse('{fileName}') done")
        print(f"Saved to {fileName}")

    def getCurrencies(self):
        self.log("API Client getCurrencies() issued")

        try:
            response = requests.post(url=self._baseUrl, params={'currencies': ''}, data={"key": self._apiKey})
        except Exception as e:
            print(f"[E] request failed: {e}")
            self.log(f"API Client getCurrencies() request failed: {e}", "Error")
            return False
        self.log(f"API Client getCurrencies() response received: {response.text}")

        try:
            parsedJson = response.json()
        except Exception as e:
            print(f"[E] bad response: {e}")
            self.log(f"API Client getCurrencies() bad response: {e}", "Error")
            return False

        if parsedJson["error"] != "":
            print(f"[E] {parsedJson['error']}")
            self.log(f"API Client getCurrencies() error: {parsedJson['error']}", "Error")
            return False

        self._currencies = parsedJson["data"]
        self.log(f"API Client getCurrencies() got: {self._currencies}")
        # print(self._currencies)
        return True

    def getExchange(self, currFrom, currTo, date):
        self.log(f"API Client getExchange('{currFrom}', '{currTo}', '{date}') issued")

        if currFrom not in self._currencies:
            print(f"[E] unknown currFrom currency: {currFrom}")
            self.log(f"API Client getExchange() unknown currFrom currency: {currFrom}", "Error")
            return

        if currTo not in self._currencies:
            print(f"[E] unknown currTo currency: {currTo}")
            self.log(f"API Client getExchange() unknown currTo currency: {currTo}", "Error")
            return

        params = {
            'from': currFrom,
            'to': currTo,
            'date': date
        }

        self.log(f"API Client POST {self._baseUrl} params={params} issued")

        try:
            response = requests.post(url=self._baseUrl, params=params, data={"key": self._apiKey})
        except Exception as e:
            print(f"[E] request failed: {e}")
            self.log(f"API Client getExchange('{currFrom}', '{currTo}', '{date}') request failed: {e}", "Error")
            return

        self.log(f"API Client getExchange('{currFrom}', '{currTo}', '{date}') response received: {response.text}")
        # print(response.text)

        try:
            parsedJson = response.json()
        except Exception as e:
            print(f"[E] bad response: {e}")
            self.log(f"API Client getExchange() bad response: {e}", "Error")
            return

        if parsedJson["error"] != "":
            print(f"[E] {parsedJson['error']}")
            self.log(f"API Client getExchange() error: {parsedJson['error']}", "Error")
            return

        self.saveResponse(currFrom, currTo, date, parsedJson)

def main():
    if len(sys.argv) != 4:
        print(f"[E] usage: python {sys.argv[0]} <from> <to> <date YYYY-MM-DD>")

        with open("full.log", "a", encoding="utf-8") as logFile:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logFile.write(f"{time}\t[Error]\tAPI Client wrong args: {sys.argv}\n")

        with open("error.log", "a", encoding="utf-8") as errorFile:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            errorFile.write(f"{time}\t[Error]\tAPI Client wrong args: {sys.argv}\n")

        return

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
