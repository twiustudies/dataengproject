from flask import Flask
import os
import time
import json
import requests
import random
import logging

# Initialize Flask application
app = Flask(__name__)

# OPTIMIZATION 1: USE LOGGING
# Set up logging to capture log messages
logging.basicConfig(level=logging.INFO)

# Configuration: Event Grid endpoint and secret key (retrieved from environment variable)
EVENT_GRID_ENDPOINT = "https://sensordata.brazilsouth-1.eventgrid.azure.net/api/events"
# OPTIMIZATION 2: use application secrets to not have sensible data in the code
EVENT_GRID_KEY = os.getenv("EVENT_GRID_KEY")  # Retrieve the Event Grid key from environment variable

# OPTIMIZATION 3: centralize timestamp generation
# Helper function to get the current UTC time in the required format
def get_current_time():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# Function to send an event to Event Grid
def send_event():
    # Ensure the EVENT_GRID_KEY environment variable is set
    if not EVENT_GRID_KEY:
        raise ValueError("Missing EVENT_GRID_KEY environment variable")

    # Set the headers for the HTTP request, including the Event Grid SAS key
    headers = {
        "Content-Type": "application/json",
        "aeg-sas-key": EVENT_GRID_KEY,  # Authorization key for Event Grid
    }

    # Generate random values for the fractions of mediums A and B
    fraction_medium_A = round(random.uniform(33, 35), 2)
    fraction_medium_B = round(100 - fraction_medium_A, 2)

    # Get the current time for the event timestamp and sample time
    current_time = get_current_time()

    # Create the event payload with the necessary fields
    event = [
        {
            "id": str(int(time.time() * 1000)),  # Unique event ID based on current timestamp (milliseconds)
            "eventType": "SensorData",  # Event type
            "subject": "sensor/abc123",  # Subject of the event (sensor identifier)
            "eventTime": current_time,  # Time of event occurrence
            "data": {
                "sensorid": "abc123",  # Sensor identifier
                "sampleTime": current_time,  # Timestamp for the sample
                "fraction medium A": fraction_medium_A,  # Fraction of medium A
                "fraction medium B": fraction_medium_B,  # Fraction of medium B
            },
            "dataVersion": "1.0"  # Version of the event data format
        }
    ]

    try:
        # Send the event to Event Grid
        response = requests.post(EVENT_GRID_ENDPOINT, headers=headers, data=json.dumps(event))
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        logging.info(f"Event sent successfully: {response.status_code}")  # Log success
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send event: {e}")  # Log failure

# Route for the root URL, just confirms the service is running
@app.route("/")
def index():
    return "Event generator is running."

# Health check route to confirm the service is up
# OPTIMIZATION 4: endpoint for health check
@app.route("/health")
def health_check():
    return "Healthy", 200  # Return HTTP status 200 if the service is healthy

# Before each request, start the event generation in a separate thread
@app.before_request
def start_event_generator():
    from threading import Thread  # Import threading module to run background tasks

    # Define the event generation function
    def generate_events():
        while True:
            send_event()  # Call the function to send an event
            time.sleep(5)  # Wait for 5 seconds before sending the next event

    # Start the event generation function in a new thread (daemonized so it runs in the background)
    Thread(target=generate_events, daemon=True).start()

