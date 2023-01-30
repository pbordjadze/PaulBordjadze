from datetime import datetime
import json

import requests

# ['id', 'eventName', 'timeEventStart', 'timeEventEnd', 'eventEnd',
# 'eventStart', 'timeBookingStart', 'timeBookingEnd', 'bookingEnd',
# 'bookingStart', 'roomID', 'room'])

# roomID 249 is Turf 1
# roomID 250 is Turf 2

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
           'referer':'https://recsports.osu.edu/fms/facilities/arc',
           'authority':'recsports.osu.edu'
           }
def open_and_closing_times(date: datetime, id):
    month=date.month
    day=date.day
    year=date.year
    url = f"https://recsports.osu.edu/fms/Home/GetHours?id={id}&startDate={month}%2F{day}%2F{year}"
    raw_json = requests.get(url, headers=headers).text
    days_hours = json.loads(raw_json)['hours']
    today = None
    for i in days_hours:
        if i['hourDate'] == f"{month}/{day}/{year}":
            today = i
            break
    if today is None:
        return None
    if today['closedAllDay'] == "true":
        return None
    #return today['openTime']
    return [datetime.strptime(today['openTime'], '%Y-%m-%dT%H:%M:%S'), datetime.strptime(today['closeTime'], '%Y-%m-%dT%H:%M:%S')]

def turf_events(month, day, year, id, field_one, field_two):
    url = f"https://recsports.osu.edu/fms/Home/GetBookings?id={id}&startDate={month}%2F{day}%2F{year}"

    raw_json = requests.get(url, headers=headers).text
    event_list = [event for event in json.loads(raw_json)["events"] if event["eventStart"] == f"{month}/{day}/{year}"]

    turf_events = [event for event in event_list if event["roomID"] == field_one or event["roomID"] == field_two]

    return turf_events
