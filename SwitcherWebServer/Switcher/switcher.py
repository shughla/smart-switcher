from SwitcherWebServer.Switcher.logger import Logger
from SwitcherWebServer.Switcher.data_store import DataStore
import paho.mqtt.client as mqtt
from time import sleep
from SwitcherWebServer.Switcher.switch import Switch
from SwitcherWebServer.Switcher.box import Box


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
        self.log_message(self.logger.get_time() + "rc: " + str(rc))

    def on_message(self, obj, msg):
        self.log_message(
            self.logger.get_time() + "topic: " + msg.topic + ". qos: " + str(msg.qos) + ". state: " + bytes(
                msg.payload).decode())

    def on_publish(self, obj, mid):
        self.log_message(self.logger.get_time() + "mid: " + str(mid))

    def on_subscribe(self, obj, mid, granted_qos):
        self.log_message(self.logger.get_time() + "Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, obj, level, message: str):
        self.log_message(self.logger.get_time() + message)

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
                self.log_message(self.logger.get_time() + "try #" + str(
                    tries) + ": Connection Refused (MQTT Server probably down)")
            if tries == self.MAX_TRIES:
                self.log_message(
                    self.logger.get_time() + "Tried connecting " + str(self.MAX_TRIES) + " times. Cannot connect.")
                break  # return in class
            tries += 1
            sleep(sleep_time)

    def log_message(self, log_message):
        self.logger.append(log_message)
        print(log_message)  # temporary

    # subscribes to all topics
    def run(self):
        self.try_connect()
        self.subscribe()
        self.loop_forever()
