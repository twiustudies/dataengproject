import os
import time
import json
import requests

# Configuration
EVENT_GRID_ENDPOINT = "https://sensordata.brazilsouth-1.eventgrid.azure.net/api/events"
EVENT_GRID_KEY = os.getenv("EVENT_GRID_KEY")  # Event Grid access key from environment variable

def send_event():
    if not EVENT_GRID_KEY:
        raise ValueError("Missing EVENT_GRID_KEY environment variable")

    headers = {
        "Content-Type": "application/json",
        "aeg-sas-key": "wRKmb5zv94LLQRFSCyxPICbDKCO24NTmLyV4tOSNegBHHYk314g3JQQJ99BAACZoyfiXJ3w3AAABAZEGDLMN"
    }

    # Event data
    event = [{
        "id": str(int(time.time() * 1000)),
        "subject": "sample-event",
        "eventType": "Sample.Created",
        "eventTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "data": {
            "message": "This is a sample event.",
            "value": 42
        },
        "dataVersion": "1.0"
    }]

    try:
        response = requests.post(EVENT_GRID_ENDPOINT, headers=headers, data=json.dumps(event))
        response.raise_for_status()
        print(f"Event sent successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send event: {e}")

if __name__ == "__main__":
    while True:
        send_event()
        time.sleep(5)
