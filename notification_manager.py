import smtplib


class NotificationManager:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_email(self, final_flight_data_list):

        links_list = []

        for dict in final_flight_data_list:
            links_list.append(f"{final_flight_data_list.index(dict)+1}) {dict['Link']}")
        #  To be better formatted in the future, will hold off for now
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs="dmmyacct410@gmail.com",
                msg=f"Subject: Flight Deals from Python!\n\n Here's the list of your deals\n{links_list}"
            )
