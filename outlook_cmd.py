import outlook
import requests

SERVER_URL="http://localhost:5000/api_schedule_weekly"
if __name__ == "__main__":
    payload = { "email": "default",
                 "startTime" : "2022-05-30T16:05",
                 "endTime" : "2022-05-30T17:05",
                 "eventTitle":"Coach AI class",
                 "days_of_week":",".join(["Monday", "Thursday"]),
                 "first_day_of_week":"Thursday",
                 "startDate":"2022-05-30",
                 "endDate":"2022-06-30"
                 }
#    outlook.schedule_event_weekly(user_email=payload["email"],
#                interval=1, days_of_week=["Monday", "Thursday"],
#                first_day_of_week="Thursday",
#                startTime = payload["startTime"],
#                endTime=payload["endTime"],
#                subject=payload["eventTitle"],
#                startDate="2022-05-30",
#                endDate="2022-06-30")
    #requests.post("https://coachai-dev.herokuapp.com/outlook_schedule", data=payload)
    requests.post(SERVER_URL, data=payload)
