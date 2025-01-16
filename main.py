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

    event = [
        {
            "id": str(int(time.time() * 1000)),
            "sensorid": "abc123",
            "eventTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "data": {
                "fraction medium A": fraction_medium_A,
                "fraction medium B": fraction_medium_B
            }
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
