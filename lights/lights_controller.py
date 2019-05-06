#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module containing function to turn on and off the lights
"""

import logging

logger    = logging.getLogger("Lights Controller")
handler   = logging.FileHandler("/tmp/snips_user_logs", mode="a", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def turn_light_on(rooms):
    """ 
    Turn on the lights on one or more room
    
    INPUT:
        - rooms <list> : list of all the room where to turn the lights on 
    """
    for room in rooms:
        logger.info("Turning lights on [room={}]".format(room))
