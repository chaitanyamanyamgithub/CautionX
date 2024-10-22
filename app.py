import os
import requests
from flask import Flask, render_template, request, jsonify
import base64

app = Flask(__name__)

# Replace with your VirusTotal API Key
API_KEY = "444ec6e96eb56f7cc57428b59b102053fc8370693394157cef5fab3c9dbf6f47"

# Helper function to encode URL to base64 as required by VirusTotal API
def encode_url_to_base64(url):
    url_bytes = url.encode('utf-8')
    return base64.urlsafe_b64encode(url_bytes).decode('utf-8').rstrip('=')

# URL Detection API call to VirusTotal
def url_detection_api(url):
    headers = {
        "x-apikey": API_KEY
    }

    encoded_url = encode_url_to_base64(url)
    api_url = f"https://www.virustotal.com/api/v3/urls/{encoded_url}"

    try:
        response = requests.get(api_url, headers=headers)

        # Check for successful response
        if response.status_code == 200:
            data = response.json()

            # Check analysis stats for malicious detection
            analysis_stats = data["data"]["attributes"]["last_analysis_stats"]
            if analysis_stats["malicious"] > 0:
                return {"message": "The URL is unsafe.", "status": "threat"}
            else:
                return {"message": "The URL is safe.", "status": "safe"}
        else:
            # Handle non-200 response codes
            return {"message": f"Error {response.status_code}: {response.json().get('error', 'Unknown Error')}", "status": "error"}
    except Exception as e:
        return {"message": f"Error contacting VirusTotal API: {str(e)}", "status": "error"}

# Dummy threat analysis for numbers
def threat_analysis_api(numbers):
    if all(num == 0 for num in numbers):  # Simulated logic: All zero numbers as threat
        return {"message": "Threat detected!", "status": "threat"}
    return {"message": "No threat detected.", "status": "safe"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/url_detection', methods=['POST'])
def url_detection():
    url = request.form.get('url')
    if url:
        result = url_detection_api(url)
        return jsonify(result)
    return jsonify({"message": "No URL provided", "status": "error"})

@app.route('/threat_analysis', methods=['POST'])
def threat_analysis():
    try:
        numbers = [int(request.form.get(f'num{i}')) for i in range(1, 5)]
        result = threat_analysis_api(numbers)
        return jsonify(result)
    except ValueError:
        return jsonify({"message": "Invalid input", "status": "error"})

if __name__ == '__main__':
    app.run(debug=True)
