#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import yaml
from hermes_python.hermes import Hermes
from lights_controller import turn_light_on

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

# Logger creation
logger    = logging.getLogger("Light Intent")
handler   = logging.FileHandler("/tmp/snips_user_logs", mode="a", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Config loading
with open("word_gender_specifier.yaml", 'r') as stream:
    try:
        word_gender_specifier = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# Utility Fonctions

def intent_received(hermes, intent_message):
    sentence = ""

    if "allumerLaLumiere" in intent_message.intent.intent_name:
        sentence = process_turn_lights_on_intent(intent_message.slots)            
    else:
        return

    hermes.publish_end_session(intent_message.session_id, sentence)


def process_turn_lights_on_intent(slots):
    """
    Process slots of the intent to and call the turn°light_on function

    INPUT:
        - slots <list> : list of all the room for which we need to turn the lights on
    OUPUT:
        - sentence <str> : the sentence to tell the user
    """
    sentence = "Ok j'allume "
    room_names = []

    # Gives all the value for the slot "room" of the intent
    room_object_list = slots.room.all()

    # There must be at least one room to light
    if len(room_object_list) == 0:
        return "Désolé mais tu n'as pas spécifié de pièce. Je ne peux rien allumer"

    # We retrieve the names of all the room to ligth
    for room in room_object_list:
        room_name = room.value
        room_names.append(room_name)

    # We got the names of all the room to light. We do the actual "light on" command
    turn_light_on(room_names)

    # Creation of the sentence for the user
    sentence_end = "{} {}".format(word_gender_specifier[room_names[-1]], room_names[-1])
    
    if len(room_names) > 1:
        for room_name in room_names[:-1]:
            sentence += "{} {} ".format(word_gender_specifier[room_name], room_name) 
        sentence += "et "
    sentence += sentence_end 
    
    return sentence



#### Main ####
with Hermes(MQTT_ADDR) as h:
    print("Starting")
    h.subscribe_intents(intent_received).start()