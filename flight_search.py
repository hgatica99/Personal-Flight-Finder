import requests


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, from_city, api_key_header, query_endpoint, flight_search_endpoint):
        self.from_city = from_city
        self.api_key = api_key_header
        self.query_endpoint = query_endpoint
        self.search_endpoint = flight_search_endpoint

    def get_flights_data(self, sheet_data, from_date, to_date):
        final_results = {}
        results_list = []

        for x in range(0, len(sheet_data["prices"])):

            search_params = {
                "fly_from": self.from_city,
                "fly_to": sheet_data["prices"][x]["iataCode"],
                "date_from": from_date,
                "curr": "USD",
                "limit": 10,
                "price_to": sheet_data["prices"][x]["lowestPrice"],
                "date_to": to_date
            }

            results = requests.get(url=self.search_endpoint, params=search_params, headers=self.api_key).json()

            # Appends dicts into a list
            results_list.append(results)

        return results_list

    #Returns a dictionary with a city and its IATA city code using a list of cities
    def get_citi_codes(self, city_list):

        city_code_dict = {}

        for city in city_list:
            query_params = {
                "term": city
            }

            query_data = requests.get(url=self.query_endpoint, params=query_params, headers=self.api_key)
            query_data.raise_for_status()

            city_code_dict[city] = query_data.json()["locations"][0]["code"]

        return city_code_dict
