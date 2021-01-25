import sys
import json
import time
from rich import print
from mqtt_common import mqtt_send_msg, mqtt_connect_broker
from mqtt_common import MQTT_BROKER_IP, MQTT_BROKER_PORT, MQTT_DEVICE_NAME
from mqtt_common import (
    MQTT_TOPIC_ALERTS,
    MQTT_TOPIC_FILES,
    MQTT_TOPIC_HELLO,
    MQTT_TOPIC_STATS,
    MQTT_TOPIC_COMMANDS,
)
from common import (
    CMD_FILE_SAVE,
    CMD_STREAMING_START,
    CMD_STREAMING_STOP,
    CMD_INFERENCE_RESTART,
)


def show_message(mqtt_client, userdata, message):
    print(f"Message received in topic: [yellow]{message.topic}[/yellow]")
    print(json.loads(message.payload.decode()))


if MQTT_BROKER_IP is None or MQTT_DEVICE_NAME is None:
    print(
        "\n[red]MQTT is DISABLED[/red]"
        " since MQTT_BROKER_IP or MQTT_DEVICE_NAME env vars are not defined\n"
    )
    sys.exit(0)

# Subscribe to some topics
print("\n[blue]Available topics:[/blue]")
print(MQTT_TOPIC_ALERTS)
print(MQTT_TOPIC_FILES)
print(MQTT_TOPIC_HELLO)
print(MQTT_TOPIC_STATS)
print(MQTT_TOPIC_COMMANDS)
topics_subscribe = []
while True:
    topic = input("\nSubscribe to topic (empty to continue): ")
    if topic == "":
        break
    topics_subscribe.append((topic, 2))  # Use qos=2

# Connect to client and subscribe
mqtt_client = mqtt_connect_broker(
    client_id="commander",
    broker_ip=MQTT_BROKER_IP,
    broker_port=MQTT_BROKER_PORT,
    subscribe_to=topics_subscribe,
)
mqtt_client.on_message = show_message

time.sleep(1)  # Wait to print connection messages
# Send commands
print("\n[blue]Available commands:[/blue]")
print(CMD_FILE_SAVE)
print(CMD_STREAMING_START)
print(CMD_STREAMING_STOP)
print(CMD_INFERENCE_RESTART)
while True:
    cmd = input("\nSend command to device (q to exit):\n")
    if cmd == "q":
        break
    payload = {"device_id": MQTT_DEVICE_NAME, "command": cmd}
    mqtt_send_msg(mqtt_client, MQTT_TOPIC_COMMANDS, payload)