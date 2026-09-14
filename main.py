import requests

class ApiClient:
    def __init__(self, baseUrl, apiKey) -> None:
        self._baseUrl = str(baseUrl)
        self._apiKey = str(apiKey)

    def saveResponse(self, fromCurr, toCurr, content):
        pass

    def log(self, msg):
        pass

    def getCurrencies(self):
        response = requests.post(url=self._baseUrl, params={'currencies': ''}, data={"key": self._apiKey})
        parsedJson = response.json()
        self._currencies = parsedJson["data"]
        print(self._currencies)

    def getExchange(self, currFrom, currTo, date):
        if currFrom not in self._currencies:
            print(f"[E] unknown currFrom currency: {currFrom}")
            return

        if currTo not in self._currencies:
            print(f"[E] unknown currTo currency: {currTo}")
            return

        params = {
            'from': currFrom,
            'to': currTo,
            'date': date
        }

        response = requests.post(url=self._baseUrl, params=params, data={"key": self._apiKey})
        print(response.text)

def main():
    # TODO: get this from .env file
    apiClient = ApiClient("http://localhost:8080", "EXAMPLE_API_KEY")
    apiClient.getCurrencies()
    apiClient.getExchange('USD', 'EUR', '2026-10-01')

main()
