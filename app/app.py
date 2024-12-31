import os
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load configuration
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set.")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.url}")

@app.after_request
def log_response_info(response):
    logging.info(f"Response: {response.status_code}")
    return response

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get city from query parameters
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required."}), 400

    try:
        # Call OpenWeatherMap API
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse API response
        data = response.json()
        return jsonify({
            "city": data.get("name"),
            "temperature": data["main"].get("temp"),
            "weather": data["weather"][0].get("description"),
            "humidity": data["main"].get("humidity"),
            "wind_speed": data["wind"].get("speed"),
        })

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err.response.text}"}), response.status_code
    except Exception as err:
        return jsonify({"error": f"An error occurred: {str(err)}"}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
