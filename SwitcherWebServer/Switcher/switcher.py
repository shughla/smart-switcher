from SwitcherWebServer.Switcher.logger import Logger
from SwitcherWebServer.Switcher.data_store import DataStore
import paho.mqtt.client as mqtt
from time import sleep
from SwitcherWebServer.Switcher.switch import Switch
from SwitcherWebServer.Switcher.box import Box

MAX_TRIES = 3
TOPIC = "switcher"  # sends something like this: index:status.

logger = Logger()


def log_message(message):
    logger.append(message)
    print(message)  # temporary


class Switcher:
    mqttc = mqtt.Client()

    def __init__(self, username, password):
        self.mqttc.on_connect = Switcher.on_connect
        self.mqttc.on_publish = Switcher.on_publish
        self.mqttc.on_subscribe = Switcher.on_subscribe
        self.mqttc.on_message = Switcher.on_message
        self.mqttc.on_disconnect = Switcher.on_disconnect
        self.mqttc.username_pw_set(username, password)

    @staticmethod
    def on_disconnect(client, userdata, rc=0):
        log_message("Disconnected with result code " + str(rc))
        client.loop_stop()

    @staticmethod
    def on_message(mqttc, obj, msg):
        log_message(
            logger.get_time() + "topic: " + msg.topic + ". qos: " + str(msg.qos) + ". state: " + bytes(
                msg.payload).decode())
        # check msg, if status error then set error flag or something similar.

    @staticmethod
    def on_log(obj, level, message: str):
        log_message(logger.get_time() + message)

    @classmethod
    def try_connect(cls, sleep_time=3):
        tries = 1
        while not cls.mqttc.is_connected():
            # mqttc.enable_logger() # need to check out
            try:
                cls.mqttc.connect("localhost", 1883, 60)
                log_message("Connected successfully.")
                break
            except ConnectionRefusedError:
                log_message(logger.get_time() + "try #" + str(
                    tries) + ": Connection Refused (MQTT Server probably down)")
            if tries == MAX_TRIES:
                log_message(
                    logger.get_time() + "Tried connecting " + str(MAX_TRIES) + " times. Cannot connect.")
                break  # return in class
            tries += 1
            sleep(sleep_time)

    @staticmethod
    def on_connect(mqttc, obj, flags, rc):
        log_message(logger.get_time() + "rc: " + str(rc))

    @staticmethod
    def on_publish(mqttc, obj, mid):
        log_message(logger.get_time() + "mid: " + str(mid))

    @staticmethod
    def on_subscribe(mqttc, obj, mid, granted_qos):
        log_message(logger.get_time() + "Subscribed: " + str(mid) + " " + str(granted_qos))

    @classmethod
    def send_message(cls, index: int, status: bool):
        message = str(index) + ":" + str(int(status))
        log_message("Sending message: [" + message + "]")
        cls.mqttc.publish(TOPIC, payload=message)
        log_message("Message has been sent.")

    # subscribes to all topics
    @classmethod
    def subscribe(cls, topic="#", qos=0):
        cls.mqttc.subscribe(topic, qos)

    @classmethod
    def start_looping(cls):
        cls.mqttc.loop_start()

    @classmethod
    def run(cls):
        cls.try_connect()
        cls.subscribe()
        cls.start_looping()  # loop forever if , meaning thread goes on forever


if __name__ == "__main__":
    logger.set_filepath("../logs/log")
    switcher = Switcher("junior", "project")
    switcher.run()  # thread is stopped here on cls.loop_forever()
    switcher.send_message(15, True)
    sleep(60)
