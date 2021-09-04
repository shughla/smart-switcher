from SwitcherWebServer.Switcher.logger import Logger
from SwitcherWebServer.Switcher.data_store import DataStore
import paho.mqtt.client as mqtt
from time import sleep

from SwitcherWebServer.Switcher.switch import Switch
from SwitcherWebServer.Switcher.box import Box

MAX_TRIES = 3
TOPIC = "switcher"  # sends something like this: index:status.

logger = Logger()

topic_index = {"switcher": 0}
index_topic = {0: "switcher"}

import sys


def terminal_print(message):
    print(message, file=sys.stderr)


def log_message(message):
    logger.append(message)
    terminal_print(message)  # temporary


class Switcher:
    data_store = DataStore()
    client = mqtt.Client()
    received_data_status = False
    received_data = dict()  # type: dict[int:list[Switch]]  # box index -> switch list

    # need to call .run() after this
    def __init__(self, username, password):
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set(username, password)

    @classmethod
    def on_message(cls, mqttc, obj, msg):
        message_value = bytes(msg.payload).decode()
        if message_value == "sensors":
            log_message(logger.get_time() + "Sending sensor update request.")
            cls.received_data_status = False
            cls.received_data = None
            return
        if message_value.startswith("c"):
            message = message_value[1:].split(":")
            switch_id = int(message[0])
            switch_state = int(message[1])
            box_index = topic_index.get(msg.topic)
            if switch_id == 0:
                log_message(logger.get_time() + "Receiving sensor checks for topic:" + msg.topic)
            log_message(logger.get_time() + "switch:" + str(switch_id) + ", status:" + str(switch_state))
            if cls.received_data is None:
                cls.received_data = dict()
            current = cls.received_data.get(box_index, [])
            current.append(Switch("", switch_id, switch_state))
            cls.received_data[box_index] = current
            if len(cls.data_store.main_data[box_index].switch_array) == switch_id + 1:
                log_message(logger.get_time() + "Switcher finished receiving sensor outputs.")
                cls.received_data_status = True
            return
        message = bytes(msg.payload).decode().split(":")
        switch_id = int(message[0])
        switch_state = int(message[1])
        cls.update_switch(topic_index[msg.topic], switch_id, switch_state)
        log_message(
            logger.get_time() + "topic: " + msg.topic + ". qos: " + str(msg.qos) +
            ". id: " + str(switch_id) + ", state: " + str(switch_state))
        # check msg, if status error then set error flag or something similar.

    @classmethod
    def check_statuses(cls, index):
        cls.client.publish(index_topic.get(index), payload="sensors")

    @classmethod
    def get_statuses(cls, index):
        if cls.received_data_status:
            cls.received_data_status = False
            return cls.received_data.get(index)
        return None

    @classmethod
    def clear_status_check(cls, box_id):
        cls.received_data_status = False
        cls.received_data = None

    @classmethod
    def on_connect(cls, mqttc, obj, flags, rc):
        log_message(logger.get_time() + "rc: " + str(rc))

    @classmethod
    def on_publish(cls, mqttc, obj, mid):
        log_message(logger.get_time() + "mid: " + str(mid))

    @classmethod
    def on_subscribe(cls, mqttc, obj, mid, granted_qos):
        log_message(logger.get_time() + "Subscribed: " + str(mid) + " " + str(granted_qos))

    @classmethod
    def on_disconnect(cls, mqttc, userdata, rc=0):
        log_message("Disconnected with result code " + str(rc))
        cls.client.loop_stop()

    @classmethod
    def update_switch(cls, box_index, index, status):
        cls.data_store.main_data[box_index].switch_array[index].status = status
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def get_data(cls):
        cls.data_store.deserialize_json()
        return cls.data_store.main_data

    @classmethod
    def save_data(cls, data=None):
        cls.data_store.serialize_json(data)

    @staticmethod
    def log(obj, level, message: str):
        log_message(logger.get_time() + message)

    @classmethod
    def get_data_store(cls):
        return cls.data_store

    @classmethod
    def remove_box(cls, box_index):
        cls.data_store.main_data.pop(box_index)
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def remove_switcher(cls, box_index, index):
        cls.data_store.main_data[box_index].switch_array.pop(index)
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def update_box_name(cls, box_index, box_name):
        cls.data_store.main_data[box_index].description = box_name
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def update_name(cls, box_index, index, name):
        cls.data_store.main_data[box_index].switch_array[index].name = name
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def get_switchers(cls, box_index):
        return cls.data_store.main_data[box_index].switch_array

    @classmethod
    def add_switcher(cls, box_index, switch: Switch):
        cls.data_store.main_data[box_index].switch_array.append(switch)
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def add_block(cls, box: Box):
        cls.data_store.main_data.append(box)
        cls.data_store.update_data(cls.data_store.main_data)

    @classmethod
    def change_data_path(cls, path):
        cls.data_store.data_file_path = path

    @classmethod
    def try_connect(cls, sleep_time=3):
        tries = 1
        while not cls.client.is_connected():
            # mqttc.enable_logger() # need to check out
            try:
                cls.client.connect("localhost", 1883, 60)
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

    @classmethod
    def switch_to(cls, index: int, status: int, topic=TOPIC):
        message = str(index) + ":" + str(int(status))
        log_message("Sending message: [" + message + "]")
        cls.client.publish(topic, payload=message)
        log_message("Message has been sent.")

    # subscribes to all topics
    @classmethod
    def subscribe(cls, topic="#", qos=0):
        cls.client.subscribe(topic, qos)

    @classmethod
    def start_looping(cls):
        cls.client.loop_start()

    @classmethod
    def get_boxes(cls):
        return cls.data_store.main_data

    @classmethod
    def run(cls, topic=TOPIC):
        cls.try_connect()
        cls.client.subscribe(topic)
        cls.start_looping()  # loop forever if , meaning thread goes on forever


if __name__ == "__main__":
    logger.set_filepath("../logs/log")
    switcher = Switcher("junior", "project")
    switcher.run()  # thread is stopped here on cls.loop_forever()
    switcher.switch_to(15, True)
    sleep(60)
