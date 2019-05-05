#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def intent_received(hermes, intent_message):
    sentence = "Vous avez demandé d'allumer la lumière "

    if intent_message.intent.intent_name == 'allumerLaLumiere':
        turn_light_on(intent_message)
    else:
        return

    hermes.publish_end_session(intent_message.session_id, sentence)


def turn_light_on(intent):
    rooms = intent.slots
    file = open("/tmp/test_log.txt","r")
    file.write("{}".format(rooms))

with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()