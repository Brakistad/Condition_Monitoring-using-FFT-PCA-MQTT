# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 14:37:43 2020

@author: oyvin
"""

import paho.mqtt.client as mqttClient;
import time as t;
from opy.kb_utils import SaveLoad as SL;

Client = mqttClient.Client("pleb");
Client.connect("192.168.192.7");
Client.publish("default", "1234");