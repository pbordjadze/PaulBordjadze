from flask import Flask, request

from design import colors
from html_generator import *
import webscraper

app = Flask(__name__)


def toDate(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d")

@app.route("/")
def homepage():
    today = request.args.get('date', default=datetime.today(), type=toDate)
    month = today.month
    day = today.day
    year = today.year
    opening_and_closing = webscraper.open_and_closing_times(today)
    events = []
    color_iter = 0
    for event in webscraper.turf_events(month, day, year):
        name = event['eventName']
        start_time = datetime.strptime(event['timeBookingStart'], '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(event['timeBookingEnd'], '%Y-%m-%dT%H:%M:%S')
        field = int(event['roomID']) - 248# roomID 249 is field 1, roomID 250 is field 2
        # for now
        events.append({
            'name':name,
            'start_time':start_time,
            'end_time':end_time,
            'field':field,
            'color':colors[color_iter % len(colors)]
        })
        color_iter += 1
    html = header_html()
    html += "<body>"
    html += title_and_date_html(today)
    html += generate_schedule(events)
    html += generate_closed_blocks(opening_and_closing)
    html += "</div>"
    html += "</body>"
    return html

