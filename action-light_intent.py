#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
from hermes_python.hermes import Hermes
from lights_controller import turn_light_on

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

logger    = logging.getLogger("Light Intent")
handler   = logging.FileHandler("/tmp/snips_user_logs", mode="a", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def intent_received(hermes, intent_message):
    sentence = "J'allume "

    if "allumerLaLumiere" in intent_message.intent.intent_name:
        rooms = process_turn_lights_on_intent(intent_message.slots)
    else:
        return

    sentence += ",".join(rooms)
    hermes.publish_end_session(intent_message.session_id, sentence)


def process_turn_lights_on_intent(slots):
    """
    Process slots of the intent to and call the turn°light_on function

    INPUT:
        - slots <list> : list of all the room for which we need to turn the lights on
    OUPUT:
        - rooms <list> : list of room's name
    """
    rooms = []
    slots_as_json = json.loads(slots)
    for slot in slots_as_json:
        if slot["slotName"] != "piece":
            logger.error("Wrong slot type for this intent [slot_type={} ; intent=allumerLaLumiere]".format(slot.slotName))
        room = slot["rawValue"]
        rooms.append(room)

    turn_light_on(rooms)
    return rooms




with Hermes(MQTT_ADDR) as h:
    print("Starting")
    h.subscribe_intents(intent_received).start()