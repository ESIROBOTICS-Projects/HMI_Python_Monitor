import psutil
import time
import paho.mqtt.client as mqtt

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

# Change to the executable's name
app_name = "E-SI.2009.exe"
monitorTopic = "HMI/Running"

def on_connect(client, userdata, flags, rc):
    time.sleep(1)
    print("Connection to broker started")

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def main():
    global mqttClient
    mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttClient.on_connect = on_connect
    
    while True:
        try:
            mqttClient.connect(MQTT_BROKER, MQTT_PORT)
            mqttClient.loop_start()
            break
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    while True:
        if is_process_running(app_name):
            print(f"{app_name} is running.")
            mqttClient.publish(monitorTopic, "true", qos=1)
        else:
            print(f"{app_name} is not running.")
            mqttClient.publish(monitorTopic, "false", qos=1)

            ##
        
        time.sleep(3)

if __name__ == "__main__":
    main()