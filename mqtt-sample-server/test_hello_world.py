"""
Test script: Publish a simple "Hello World" print job to the MQTT broker.
Run this after starting mqtt_server.py and connecting the printer.
"""
import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

# Printer configuration (must match ClientTools MQTT Cloud tab)
PRINTER_DEVICE_ID = "111222555"
BROKER_HOST = "127.0.0.1"  # Use localhost since broker runs on same laptop
BROKER_PORT = 9883
USERNAME = "user"
PASSWORD = "user123"

# Topic the printer subscribes to (receives print data)
TOPIC_DATA = f"/sys/{PRINTER_DEVICE_ID}/user/data"
# Topic the printer publishes to (sends status)
TOPIC_STATUS = f"/sys/{PRINTER_DEVICE_ID}/user/status"


def build_hello_world_payload():
    payload = bytes([
        0x1B, 0x40,        # Initialize printer
        0x1B, 0x61, 0x01,  # Center align
    ]) + b"Hello World!\n\n" + bytes([0x1d, 0x56, 0x42, 0x00])
    return payload

# def build_hello_world_payload():
#     payload = bytes([
#         0x1B, 0x40,        # Initialize printer
#         0x1B, 0x61, 0x01,  # Center align
#     ]) + b"Hello World!" + bytes([0x0a, 0x1b, 0x69])
#     return payload


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker!")
        client.subscribe(TOPIC_STATUS)
        print(f"Subscribed to status topic: {TOPIC_STATUS}")
    else:
        print(f"Failed to connect, reason code: {reason_code}")


def on_message(client, userdata, msg):
    print(f"[Status from printer] {msg.topic}: {msg.payload}")


def main():
    client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id="test_publisher_" + str(int(time.time()))
    )
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker: {BROKER_HOST}:{BROKER_PORT}")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    # Wait for connection
    time.sleep(1)

    # Build and publish the print payload
    payload = build_hello_world_payload()
    print(f"Publishing {len(payload)} bytes to {TOPIC_DATA}")
    result = client.publish(TOPIC_DATA, payload, qos=1)
    result.wait_for_publish()
    print("Print job published!")

    # Wait to see if printer sends status back
    print("Waiting 3 seconds for printer status...")
    time.sleep(3)

    client.loop_stop()
    client.disconnect()
    print("Done.")


if __name__ == "__main__":
    main()
