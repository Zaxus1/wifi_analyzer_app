from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from wifi_scanner import get_aps, get_distance
from map_creator import create_map

app = Flask(__name__)

# Enable CORS for your frontend application
CORS(app, origins="http://192.168.104.171:8081")

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)  # Log to a file

# Define the route to get access points


@app.route('/get_aps', methods=['GET'])
def get_access_points():
    try:
        nearby_aps = get_aps()
        return jsonify({'access_points': nearby_aps}), 200
    except Exception as e:
        app.logger.error(str(e))  # Log detailed error message
        return jsonify({'error': 'Internal server error'}), 500

# Define the route to get access point distance


@app.route('/get_distance', methods=['GET', 'POST'])
def get_access_point_distance():
    try:
        ap_mac = request.args.get('ap_mac')
        if ap_mac is None:
            return jsonify({'error': 'ap_mac parameter is missing'}), 400

        ap_rssi, distance = get_distance(ap_mac)
        return jsonify({'ap_rssi': ap_rssi, 'distance': distance}), 200
    except Exception as e:
        app.logger.error(str(e))  # Log detailed error message
        return jsonify({'error': 'Internal server error'}), 500

# Define the route to create an obstacle map


@app.route('/create_map', methods=['POST'])
def create_obstacle_map():
    try:
        data = request.json

        app.logger.debug("Received data: %s", data)  # Log received data

        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400

        ap_x = data.get('ap_x')
        ap_y = data.get('ap_y')
        map_dir = data.get('map_dir')

        if ap_x is None or ap_y is None or map_dir is None:
            return jsonify({'error': 'Missing required data fields'}), 400

        create_map(ap_x, ap_y, map_dir)  # type: ignore
        return jsonify({'message': 'Map created successfully'}), 200
    except Exception as e:
        app.logger.error(str(e))  # Log detailed error message
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=8000)
