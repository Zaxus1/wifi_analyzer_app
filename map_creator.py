from PIL import Image
import matplotlib.pyplot as plt
import requests
from math import sqrt, e, sin, cos, atan, fabs, pi
from matplotlib.colors import LinearSegmentedColormap

# Function to get location coordinates based on a location name


def get_location_coordinates(location_name):
    try:
        # Use a geocoding service to get latitude and longitude based on location name
        geocoding_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location_name}"
        response = requests.get(geocoding_url)
        data = response.json()
        if data and len(data) > 0:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print(f"Error getting location coordinates: {str(e)}")
        return None

# Function to create a heatmap


def create_map(latitude, longitude):
    try:
        # Use latitude and longitude to dynamically fetch a map image
        map_dir = f"https://api.maptiler.com/maps/streets-v2/static/{latitude},{longitude},7/400x300@2x.png?key=79NlHfEi2LJ3D7UjsbpE"

        response = requests.get(map_dir)
        if response.status_code == 200:
            with open("map_image.png", "wb") as file:
                file.write(response.content)

            obstacle_map = Image.open("map_image.png")
            width, height = obstacle_map.size
            rgb_map = obstacle_map.convert("RGB")
            rssi_map = {}
            ap_x = latitude  # Set the AP x-coordinate based on latitude
            ap_y = longitude  # Set the AP y-coordinate based on longitude

            for x in range(width):
                for y in range(height):
                    r, g, b = rgb_map.getpixel((x, y))
                    if r == g == b == 0:
                        rssi_map[(x, y)] = -1
                        continue
                    dy = x - ap_x
                    dx = y - ap_y
                    distance = sqrt(dy**2 + dx**2) / 10
                    # Replace with your equation
                    raw_rssi = e ** (-0.232584 * distance) * \
                        (87.4389 - 81 * e ** (0.232584 * distance))
                    adjusted_rssi = raw_rssi - \
                        get_path_obstacle(rgb_map, x, y, ap_x, ap_y)
                    rssi_map[(x, y)] = adjusted_rssi
            draw_heat_map(rssi_map, -90, -30, width, height)
        else:
            print('Error fetching map image.')
    except Exception as e:
        print(f"Error creating heat map: {str(e)}")

# Function to detect obstacles along the path


def get_path_obstacle(rgb_map, x1, y1, x2, y2):
    rssi_subtract = 0
    dx = x2 - x1
    dy = y2 - y1
    px_distance = sqrt(dy**2 + dx**2)
    path_angle = fabs(atan(dy / dx)) if not dx == 0 else pi / 2
    x_neg = dx < 0
    y_neg = dy < 0
    for path_distance in range(int(px_distance)):
        path_x = path_distance * cos(path_angle) * (-1 if x_neg else 1)
        path_y = path_distance * sin(path_angle) * (-1 if y_neg else 1)
        path_x = path_x + x1
        path_y = path_y + y1
        # Ensure coordinates are integers
        r, g, b = rgb_map.getpixel((int(path_x), int(path_y)))
        if b - r > 30 and g - r > 30:
            rssi_subtract += 2
        elif r - g > 30 and r - b > 30:
            rssi_subtract += 8
        elif g - r > 30 and g - b > 30:
            rssi_subtract += 6
        elif b - r > 30 and b - g > 30:
            rssi_subtract += 4
    return rssi_subtract

# Function to draw a heatmap


def draw_heat_map(rssi_map, min_val, max_val, width, height):
    cmap = LinearSegmentedColormap.from_list(
        'custom_cmap', [(0, 'black'), (1, 'red')])
    heat_map = plt.imshow([[0, 0], [0, 0]], cmap=cmap)
    heat_map.set_data([[rssi_map[(x, y)] for y in range(height)]
                      for x in range(width)])
    plt.colorbar(heat_map)
    plt.show()


def main():
    location_name = input("Enter the location name (e.g., city or address): ")
    location_coordinates = get_location_coordinates(location_name)

    if location_coordinates:
        latitude, longitude = location_coordinates
        print(
            f"Location Coordinates - Latitude: {latitude}, Longitude: {longitude}")
        create_map(latitude, longitude)
    else:
        print('Location not found.')


if __name__ == '__main__':
    main()
