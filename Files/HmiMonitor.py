import psutil
import time
import paho.mqtt.client as mqtt
import argparse

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

# Change to the executable's name
hmi_name = ""
monitorTopic = "HMI/Running"

parser = argparse.ArgumentParser(description='HmiName')
parser.add_argument('--hmi_name', type=str, help='The name of the executable file for the HMI', required=True)
args = parser.parse_args()
hmi_name = args.hmi_name
print(f'Executable name to monitor: {hmi_name}')

def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")
    while True:
        try:
            print("Attempting to reconnect...")
            client.reconnect()
            break
        except Exception as e:
            print(f"Reconnection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def is_process_running(processName):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == processName:
                return True
        return False
    except psutil.Error as e:
        print(f"Error checking process status: {e}")
        return False

def main():
    global mqttClient
    mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttClient.on_connect = on_connect
    mqttClient.on_disconnect = on_disconnect
    
    while True:
        try:
            mqttClient.connect(MQTT_BROKER, MQTT_PORT)
            mqttClient.loop_start()
            break
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    while True:
        if (mqttClient.is_connected):
            if is_process_running(hmi_name):
                print(f"{hmi_name} is running.")
                mqttClient.publish(monitorTopic, "true", qos=1)
            else:
                print(f"{hmi_name} is not running.")
                mqttClient.publish(monitorTopic, "false", qos=1)

                ##!Robo
        
        time.sleep(3)

if __name__ == "__main__":
    main()