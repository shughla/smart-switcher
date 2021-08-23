import paho.mqtt.client as mqtt
import logger as logger_cls
import time

MAX_TRIES = 5


def on_connect(mqtt_cl, obj, flags, rc):
    log = time.ctime() + " - rc: " + str(rc)
    logger.append(log)
    print(log)


def on_message(mqtt_cl, obj, msg):
    log = time.ctime() + " - topic: " + msg.topic + ". qos: " + str(msg.qos) + ". state: " + bytes(msg.payload).decode()
    logger.append(log)
    print(log)


def on_publish(mqtt_cl, obj, mid):
    log = time.ctime() + " - mid: " + str(mid)
    logger.append(log)
    print(log)


def on_subscribe(mqtt_cl, obj, mid, granted_qos):
    log = time.ctime() + " - Subscribed: " + str(mid) + " " + str(granted_qos)
    logger.append(log)
    print(log)


def on_log(mqtt_cl, obj, level, string):
    string = time.ctime() + " - " + string
    logger.append(string)
    print(string)


def set_mqtt(mqtt_cl):
    # If you want to use a specific client id, use
    # mqttc = mqtt.Client("client-id")
    # but note that the client id must be unique on the broker. Leaving the client
    # id parameter empty will generate a random id for you.
    mqtt_cl.on_message = on_message
    mqtt_cl.on_connect = on_connect
    mqtt_cl.on_publish = on_publish
    mqtt_cl.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
    mqttc.username_pw_set("junior", "project")


if __name__ == '__main__':
    logger = logger_cls.Logger
    mqttc = mqtt.Client()
    set_mqtt(mqttc)
    tries = 1
    while not mqttc.is_connected():
        # mqttc.enable_logger() # need to check out
        try:
            mqttc.connect("localhost", 1883, 60)
        except ConnectionRefusedError:
            log_msg = time.ctime() + " - try #" + str(tries) + ": Connection Refused (MQTT Server probably down)"
            logger.append(log_msg)
            print(log_msg)
        if tries == MAX_TRIES:
            break
        tries += 1
        time.sleep(5)
    mqttc.subscribe("#", 0)
    mqttc.loop_forever()
