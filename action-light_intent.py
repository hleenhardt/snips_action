#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def intent_received(hermes, intent_message):
    sentence = "Vous avez demande d'allumer la lumiere "

    file = open("/tmp/test_log.txt","r")
    file.write("{}".format(intent_message))
    file.close()
    #if intent_message.intent.intent_name == "allumerLaLumiere":
    #    print("Hello")
    #else:
    #    return

    hermes.publish_end_session(intent_message.session_id, sentence)


with Hermes(MQTT_ADDR) as h:
    print("Starting")
    h.subscribe_intents(intent_received).start()