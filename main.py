from flask import Flask
import os
import time
import json
import requests
import random

app = Flask(__name__)

# Configuration
EVENT_GRID_ENDPOINT = "https://sensordata.brazilsouth-1.eventgrid.azure.net/api/events"
EVENT_GRID_KEY = "wRKmb5zv94LLQRFSCyxPICbDKCO24NTmLyV4tOSNegBHHYk314g3JQQJ99BAACZoyfiXJ3w3AAABAZEGDLMN"  # Event Grid access key from environment variable


def send_event():
    if not EVENT_GRID_KEY:
        raise ValueError("Missing EVENT_GRID_KEY environment variable")

    headers = {
        "Content-Type": "application/json",
        "aeg-sas-key": EVENT_GRID_KEY,
    }

    # Calculate "fraction medium A" first
    fraction_medium_A = round(random.uniform(33, 35), 2)
    # Calculate "fraction medium B" as the remainder to make the total 100
    fraction_medium_B = round(100 - fraction_medium_A, 2)
    eventtime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    event = [
        {
            "id": str(int(time.time() * 1000)),
            "eventType": "SensorData",
            "subject": "sensor/abc123",
            "eventTime": eventtime,
            "data": {
                "eventTime": eventtime,
                "sensorid": "abc123",
                "fraction medium A": fraction_medium_A,
                "fraction medium B": fraction_medium_B
            },
            "dataVersion": "1.0"
        }
    ]

    try:
        response = requests.post(EVENT_GRID_ENDPOINT, headers=headers, data=json.dumps(event))
        response.raise_for_status()
        print(f"Event sent successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send event: {e}")


@app.route("/")
def index():
    return "Event generator is running."


@app.before_request
def start_event_generator():
    from threading import Thread

    def generate_events():
        while True:
            send_event()
            time.sleep(5)

    Thread(target=generate_events, daemon=True).start()