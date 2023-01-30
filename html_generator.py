from datetime import datetime, timedelta
import typing as t
from design import closed_color

def generate_closed_blocks(times: t.List):
    if len(times) == 0:
        html = f'<p class="closed" style="background-color: {closed_color}; grid-row: 2 / 74; grid-column: 2 / 3">ARC CLOSED ALL DAY</p>\n'
    else:
        base = datetime(1900, 1, 1, 6)
        open = round_to_nearest_15(times[0])
        close = round_to_nearest_15(times[1])
        open_row = ((open - base) / timedelta(minutes=15)) + 2
        close_row = ((close - base) / timedelta(minutes=15)) + 2
        open_string = times[0].strftime("%I:%M %p")
        close_string = times[1].strftime("%I:%M %p")
        html = ""
        if open > base:
            html += f'<p class="closed" style="background-color: {closed_color}; grid-row: 2 / {int(open_row)}; grid-column: 2 / 4">ARC CLOSED UNTIL<br>{open_string}</p>\n'
        if close != datetime(1900, 1, 1, 0):
            html += f'<p class="closed" style="background-color: {closed_color}; grid-row: {int(close_row)} / 79; grid-column: 2 / 4">ARC CLOSES AT<br>{close_string}</p>\n'
    return html


def round_to_nearest_15(dt: datetime):
    dt = dt - timedelta(minutes=dt.minute % 15)
    return datetime(1900, 1, 1, dt.hour, dt.minute)

def header_html():
    html = """
    <header>
    <meta charset="UTF-8">
    <title>Turf Schedule</title>
    <link rel="stylesheet" type="text/css" href="static/stylesheets/schedule_style.css"/>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Nunito">
    </header>
    """
    return html

def title_and_date_html(date_of_page: datetime):
    today = datetime.today()
    today_link = today.strftime('/?date=%Y-%m-%d')
    previous = tomorrow = date_of_page - timedelta(days=1)
    previous_link = previous.strftime('/?date=%Y-%m-%d')
    tomorrow = date_of_page + timedelta(days=1)
    tomorrow_link = tomorrow.strftime('/?date=%Y-%m-%d')
    html = f"""
    <p class="main-title">ARC Turf Fields Status</p>
    <p class="main-title">{date_of_page.strftime('%A, %b %d %Y')}</p>
    <div class="buttons">
    <button class="button-3" style="grid-row: 1; grid-column: 1" "role="button" onclick="window.location.href='{previous_link}'">Previous</button>
    <button class="button-3" style="grid-row: 1; grid-column: 2" role="button" onclick="window.location.href='{today_link}'">Today</button>
    <button class="button-3" style="grid-row: 1; grid-column: 3" role="button" onclick="window.location.href='{tomorrow_link}'">Next</button>
    </div>
    """
    return html

def generate_event(event: t.Dict):
    base = datetime(1900, 1, 1, 6)
    start = round_to_nearest_15(event['start_time'])
    end = round_to_nearest_15(event['end_time'])
    start_row = ((start - base)/timedelta(minutes=15)) + 2
    end_row = ((end - base)/timedelta(minutes=15)) + 2
    if end == datetime(1900, 1, 1, 0):
        end_row = 79
    time_string = event['start_time'].strftime("%I:%M %p") + " - " + event['end_time'].strftime("%I:%M %p")

    html = f'<p class="event" style="background-color: {event["color"]}; grid-row: {int(start_row)} / {int(end_row)}; grid-column: {event["field"] + 1}">{event["name"]}<br>{time_string}</p>\n'
    return html

def generate_schedule(events: t.List[t.Dict], open_time=None, close_time=None):
    visible_times = {round_to_nearest_15(event['start_time']) for event in events}
    visible_times.update({round_to_nearest_15(event['end_time']) for event in events})
    visible_times.add(open_time)
    visible_times.add(close_time)
    for i in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
        visible_times.add(datetime(1900, 1, 1, i))
    visible_times.add(datetime(1900, 1, 2, 0))


    html = """
    <div class="schedule">
    <span class="field" style="grid-row: 1; grid-column: 2">Field 1</span>
    <span class="field" style="grid-row: 1; grid-column: 3">Field 2</span>\n"""
    time = datetime(1900, 1, 1, 6)
    for i in range(2, 75):
        visible = ""
        if time in visible_times:
            visible = "visibility: visible; "
        html += f'\t\t<p class="time-row" style="{visible}grid-row: {i}; grid-column: 1">{time.strftime("%I:%M %p")}</p>\n'
        time += timedelta(minutes=15)
    for i in range(75, 80):
        html += f'<p class="time-row" style="grid-row: {i}; grid-column: 1">buffer</p>'
    # One extra row just looks nicer
    for event in events:
        html += generate_event(event)


    return html
