# Event Generator with Flask and Azure Event Grid

This repository contains a Python application that generates sensor data events and sends them to an Azure Event Grid endpoint. The application uses Flask to run a web server and periodically sends events to the configured Event Grid endpoint.

# Prerequisites

Python 3.8 or higher
Flask
Requests library
Setup

## Clone the repository:

git clone <repository-url>
cd <repository-directory>
Install dependencies:

pip install -r requirements.txt
## Configure Event Grid:

Update the EVENT_GRID_ENDPOINT and EVENT_GRID_KEY variables in the code with your Azure Event Grid endpoint and access key.
Running the Application

## Set the environment variable for the Event Grid key:

export EVENT_GRID_KEY=<your-event-grid-key>

## Event Generation

The application generates sensor data events every 5 seconds. Each event includes:

fraction medium A: A random value between 33 and 35.
fraction medium B: The remainder to make the total 100.
## Event Sending

The events are sent to the configured Azure Event Grid endpoint using the requests library. The application logs the status of each event sent.

## Flask Web Server

The Flask web server runs and provides a simple endpoint to indicate that the event generator is running.

## Error Handling

If the Event Grid key is missing or the event sending fails, appropriate error messages are logged.

## License

This project is licensed under the MIT License.

## Additional

To build the application in Azure, see the DOCKERFILE.
