class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, possible_flights):
        self.flights = possible_flights

    def get_final_flight_data(self):
        list_of_final_data = []

        # Check to see if there is data to be analyzed from the json file. If None, there was no match for our flight
        # parameters, else, look for specific data to be sent via email

        for x in range(0, len(self.flights)):

            if self.flights[x]["data"] is None:
                print("No data found")
            else:
                for y in range(0, len(self.flights[x]["data"])):
                    link = self.flights[x]["data"][y]["deep_link"]
                    final_city_from = self.flights[x]["data"][y]["cityFrom"]
                    final_city_to = self.flights[x]["data"][y]["cityTo"]
                    flight_price = self.flights[x]["data"][y]["price"]

                    temp_dict = {
                        "From": final_city_from,
                        "To": final_city_to,
                        "Price": flight_price,
                        "Link": link

                    }
                    # Instead of a list, I nested dictionaries for ease of data retrieval needed when sending emails
                    list_of_final_data.append(temp_dict)

        return list_of_final_data