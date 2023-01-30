from flask import Flask, request, render_template

from design import colors
from html_generator import *
import webscraper

app = Flask(__name__)


def toDate(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d")

@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/calendar<id>/") # ARC, JOS, or LTP
def calendar(id):
    today = request.args.get('date', default=datetime.today(), type=toDate)
    month = today.month
    day = today.day
    year = today.year
    other_ids = ["ARC", "JOS", "LTP"]
    if id == "ARC":
        location_id = 1
        field_one_id = 249
        field_two_id = 250
    elif id == "LTP":
        location_id = 10
        field_one_id = 386 # NE Turf Field
        field_two_id = 384 # NW Turf Field
    elif id == "JOS":
        location_id = 4
        field_one_id = 0
        field_two_id = 322
    else:
        id = "ARC"
        location_id = 1
        field_one_id = 249
        field_two_id = 250
    other_ids.remove(id)


    opening_and_closing = webscraper.open_and_closing_times(today, location_id)
    events = []
    color_iter = 0
    for event in webscraper.turf_events(month, day, year, location_id, field_one_id, field_two_id):
        name = event['eventName']
        start_time = datetime.strptime(event['timeBookingStart'], '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(event['timeBookingEnd'], '%Y-%m-%dT%H:%M:%S')
        if int(event['roomID']) == field_one_id:
            field = 1
        elif int(event['roomID']) == field_two_id:
            field = 2
        else:
            raise Exception("roomID from the webscraper doesn't match the roomIDs in app.py")
        events.append({
            'name':name,
            'start_time':start_time,
            'end_time':end_time,
            'field':field,
            'color':colors[color_iter % len(colors)]
        })
        color_iter += 1
    html = header_html(id)
    html += "<body>"
    html += title_and_date_html(today, id)
    html += generate_schedule(events)
    html += generate_closed_blocks(opening_and_closing, id)
    html += "</div>"
    html += generate_footer(other_ids)
    html += "</body>"
    return html

