import requests


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, sheety_endpoint):
        self.endpoint = sheety_endpoint

    def get_row_data(self):
        data = requests.get(url=self.endpoint)
        data.raise_for_status()
        return data

    def update_sheet_iata(self, city_pairs, city_list):
        for x in range(0, len(city_list)):

            json_load = {
                "price": {
                        "city": city_list[x],
                        "iataCode": city_pairs[city_list[x]],
                    }
            }

            update_request = requests.put(url=f"{self.endpoint}/{x+2}", json=json_load)
            update_request.raise_for_status()
