import paho.mqtt.client as mqtt
import logger as logger_cls
import time
if __name__ == '__main__':
    logger = logger_cls.Logger


def on_connect(mqttc, obj, flags, rc):
    log = time.ctime() + " - rc: " + str(rc)
    logger.append(log)
    print(log)


def on_message(mqttc, obj, msg):
    log = time.ctime() + " - topic: " + msg.topic + ". qos: " + str(msg.qos) + ". state: " + bytes(msg.payload).decode()
    logger.append(log)
    print(log)


def on_publish(mqttc, obj, mid):
    log = time.ctime() + " - mid: " + str(mid)
    logger.append(log)
    print(log)


def on_subscribe(mqttc, obj, mid, granted_qos):
    log = time.ctime() + " - Subscribed: " + str(mid) + " " + str(granted_qos)
    logger.append(log)
    print(log)


def on_log(mqttc, obj, level, string):
    string = time.ctime() + " - " + string
    logger.append(string)
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.username_pw_set("junior", "project")
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("#", 0)

mqttc.loop_forever()
