import os;
from dotenv import load_dotenv;
import requests


load_dotenv()


class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"];
        self._api_secret = os.environ["AMADEUS_API_SECRET"];
        self._amadeus_enpoint =  os.environ["AMADEUS_ENDPOINT"];
        self._iata_endpoint = os.environ["IATA_ENDPOINT"]
        self._token = self._get_new_token();


    def get_iata_code(self, city_name):
        return "TESTING";


    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url = self._amadeus_enpoint, 
                                 headers= header, data=body)
        print(f"Your token is {response.json()['access_token']}");
        print(f"Your token expires in {response.json()['expires_in']} seconds");
        return response.json()['access_token'];

    def get_destination_code(self, city_name):
        print(f"Using this token to get destination {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(
            url= self._iata_endpoint,
            headers=headers,
            params=query
        )
        
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code


# FlightSearch()