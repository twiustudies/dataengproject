import time
import json
import random
import requests
from datetime import datetime

# Function to generate random percentages
def generate_random_percentage():
    return round(random.uniform(0, 100), 2)

# Function to create the event data
def create_event():
    event = {
        "sensor-id": "abc123",
        "medium-A-fraction": generate_random_percentage(),
        "medium-B-fraction": generate_random_percentage(),
        "eventTime": datetime.utcnow().isoformat()
    }
    return event

# Function to send the event to Azure Event Grid
def send_event(event):
    url = "https://sensordata.brazilsouth-1.eventgrid.azure.net/api/events"
    headers = {
        "Content-Type": "application/json",
        "aeg-sas-key": "wRKmb5zv94LLQRFSCyxPICbDKCO24NTmLyV4tOSNegBHHYk314g3JQQJ99BAACZoyfiXJ3w3AAABAZEGDLMN"  # Replace with your Event Grid key
    }
    response = requests.post(url, headers=headers, data=json.dumps([event]))
    if response.status_code == 200:
        print("Event sent successfully")
    else:
        print(f"Failed to send event: {response.status_code}, {response.text}")

# Main loop to generate and send events every 5 seconds
while True:
    event = create_event()
    send_event(event)
    time.sleep(5)
