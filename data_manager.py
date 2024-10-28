import os;
import requests;
from dotenv import load_dotenv;
load_dotenv()

class DataManager:
    def __init__(self):
        self.END_POINT = os.environ["ENDPOINT"];
    
    
    def update_iata_code(self, row_id, iata_code):
        update_endpoint = f"{self.END_POINT}/{row_id}"

        new_data = {
            "price":{
                "iataCode": iata_code
            }
        }

        response = requests.put(update_endpoint, json = new_data);
        response.raise_for_status();
        print(response)

    def get_destination_data(self):
        response = requests.get(url=self.END_POINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data
    

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.END_POINT}/{city['id']}",
                json=new_data
            )
            print(response.text)