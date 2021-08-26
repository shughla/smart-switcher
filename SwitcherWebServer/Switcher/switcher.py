from SwitcherWebServer.Switcher.logger import Logger
import paho.mqtt.client as mqtt
from time import sleep


class Switcher:
    MAX_TRIES = 3
    mqttc = mqtt.Client()
    logger = Logger

    def __init__(self, username, password):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.username_pw_set(username, password)

    def on_connect(self, obj, flags, rc):
        log = self.logger.get_time() + "rc: " + str(rc)  # mqtt_cl.connack_string(rc)
        self.logger.append(log)
        print(log)

    def on_message(self, obj, msg):
        log = self.logger.get_time() + "topic: " + msg.topic + ". qos: " + str(msg.qos) + ". state: " + bytes(
            msg.payload).decode()
        self.logger.append(log)
        print(log)

    def on_publish(self, obj, mid):
        log = self.logger.get_time() + "mid: " + str(mid)
        self.logger.append(log)
        print(log)

    def on_subscribe(self, obj, mid, granted_qos):
        log = self.logger.get_time() + "Subscribed: " + str(mid) + " " + str(granted_qos)
        self.logger.append(log)
        print(log)

    def on_log(self, obj, level, string):
        string = self.logger.get_time() + string
        self.logger.append(string)
        print(string)

    def subscribe(self, topic="#", qos=0):
        self.mqttc.subscribe(topic, qos)

    def loop_forever(self):
        self.mqttc.loop_forever()

    def try_connect(self, max_tries=3, sleep_time=3):
        self.MAX_TRIES = max_tries
        tries = 1
        while not self.mqttc.is_connected():
            # mqttc.enable_logger() # need to check out
            try:
                self.mqttc.connect("localhost", 1883, 60)
            except ConnectionRefusedError:
                log_msg = self.logger.get_time() + "try #" + str(
                    tries) + ": Connection Refused (MQTT Server probably down)"
                self.logger.append(log_msg)
                print(log_msg)
            if tries == self.MAX_TRIES:
                log_msg = self.logger.get_time() + "Tried connecting " + str(self.MAX_TRIES) + " times. Cannot connect."
                self.logger.append(log_msg)
                print(log_msg)
                break  # return in class
            tries += 1
            sleep(sleep_time)

    # subscribes to all topics
    def run(self):
        self.try_connect()
        self.subscribe()
        self.loop_forever()
