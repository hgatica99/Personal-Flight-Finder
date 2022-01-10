import os
from datetime import datetime as dt
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

TEQUILA_SEARCH_FLIGHT_ENDPOINT = os.environ.get("TEQUILA_SEARCH_FLIGHT_ENDPOINT")
TEQUILA_LOCATION_QUERY_ENDPOINT = os.environ.get("TEQUILA_LOCATION_QUERY_ENDPOINT")
MY_CITY_CODE = "NYC"

MY_EMAIL = os.environ.get("TEST_EMAIL")
MY_EMAIL_PASSWORD = os.environ.get("TEST_EMAIL_PASSWORD")

TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

TODAYS_DATE = todays_date = dt.today().date()
CURRENT_YEAR = TODAYS_DATE.year
CURRENT_MONTH = TODAYS_DATE.month
CURRENT_DAY = TODAYS_DATE.day
CURRENT_FORMATTED_DATE = f"{CURRENT_DAY}/{CURRENT_MONTH}/{CURRENT_YEAR}"
FUTURE_DATE = "will be replaced once datautil is working"

# ___________________________________________________________________________________
tequila_api_key = {
    "apikey": TEQUILA_API_KEY
}
# ____________________________________________________________________________________

# I need to Get existing data from google sheets using data_manager to find and update CITY/IATA code using
# flight_search
data_manager1 = DataManager(sheety_endpoint=SHEETY_ENDPOINT)

flight_searcher = FlightSearch(from_city=MY_CITY_CODE,
                               api_key_header=tequila_api_key,
                               query_endpoint=TEQUILA_LOCATION_QUERY_ENDPOINT,
                               flight_search_endpoint=TEQUILA_SEARCH_FLIGHT_ENDPOINT)

# Gets the preexisting rows to be updated
row_data = data_manager1.get_row_data().json()

city_list = [city["city"] for city in row_data["prices"]]

# Uses preexisting rows to find missing CITY/IATA codes
city_code_pairs = flight_searcher.get_citi_codes(city_list)

# Once codes are found, sheet is populated
data_manager1.update_sheet_iata(city_pairs=city_code_pairs, city_list=city_list)

# updating row_data to included updated IATA codes tied to cities, to be used for flight searching
row_data = data_manager1.get_row_data().json()

# Need to search for flights that match our criteria. Raw json data is then sent to FlightData Object to be analyzed
possible_flights = flight_searcher.get_flights_data(sheet_data=row_data, from_date=CURRENT_FORMATTED_DATE, to_date="26/06/2022")

# Setsup the data anylzer with the flights that match our criteria
flight_data_analyzer = FlightData(possible_flights=possible_flights)

final_flight_data = flight_data_analyzer.get_final_flight_data()

emailer = NotificationManager(email=MY_EMAIL, password=MY_EMAIL_PASSWORD)

emailer.send_email(final_flight_data_list=final_flight_data)

