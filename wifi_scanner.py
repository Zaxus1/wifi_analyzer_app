import pywifi
import time
import json
from math import log10
import requests

import uuid


def list_wifi_interfaces():
    # List available WiFi interfaces
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()

    if not interfaces:
        print("No WiFi interfaces found.")
        return []

    print("Available WiFi Interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"Interface {i}: {iface.name()}")

    return interfaces


def get_mac_address():
    # Get the MAC address of the WiFi interface
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(0.5)
    iface.scan()
    time.sleep(1)
    scan_results = iface.scan_results()

    for result in scan_results:
        ssid = result.ssid
        bssid = result.bssid
        if ssid and bssid:
            return bssid.lower()
    return None


def get_aps():
    # Get a list of nearby Access Points (APs) and their information
    print("hello")
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    print(iface)
    iface.scan()
    time.sleep(1.5)
    scan_out_data = {}
    scan_out_results = iface.scan_results()
    print(scan_out_results)

    for result in scan_out_results:
        ssid = result.ssid
        bssid = result.bssid.lower()
        rssi = result.signal
        scan_out_data[bssid] = {"SSID": ssid, "RSSI": rssi}
    print(scan_out_data)
    return scan_out_data


def get_distance(ap_mac):
    # Calculate the distance to a specific Access Point (AP) based on RSSI
    nearby_aps = get_aps()
    if ap_mac is None:
        print("MAC Address of the Wi-Fi interface not found")
        # return -1, None
    if ap_mac not in nearby_aps.keys():
        print("Specified Access Point Not Found!")
        # return -1, None
    ap_rssi = nearby_aps[ap_mac]["RSSI"]
    distance = -log10(2 * ((ap_rssi + 160) ** 9.9)) + 50
    return ap_rssi, distance


def send_data_to_server(ap_mac):
    # Send data (AP MAC address) to a server and receive RSSI and distance
    try:
        server_url = f'http://192.168.104.171:8000/get_distance?ap_mac={ap_mac}'
        response = requests.post(server_url)
        if response.status_code == 200:
            result = response.json()
            ap_rssi = result['ap_rssi']
            distance = result['distance']
            return ap_rssi, distance
        else:
            return None, None
    except Exception as e:
        print(f"Error sending data to server: {str(e)}")
        return None, None


if __name__ == '__main__':
    get_aps()

    mac_address = uuid.getnode()
    # ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
    ap_mac = 'ba:dd:71:e5:a9:4e:'
    if 'ba:dd:71:e5:a9:4e:' in get_aps():
        print("hi")
    else:
        print("bye")
    # ap_mac = input("Enter the MAC address of the Access Point (AP): ")
    print(ap_mac)
    ap_rssi, distance = send_data_to_server(ap_mac)
    time.sleep(2)
    if ap_rssi is not None and distance is not None:
        print(f"RSSI: {ap_rssi} dBm, Distance: {distance} meters")
    else:
        print("Error getting RSSI and distance. Please check the MAC address or try again later.")
