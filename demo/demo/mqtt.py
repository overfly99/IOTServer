from paho.mqtt import client as mqtt_client
import json
from decouple import config

import django
django.setup()
from smart_home.tasks import *
from smart_home.models import *


topic = 'overfly_99/home'
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    
    home = eval(msg.payload.decode())
    try:
        id = home["id"]
        temperature = home['temperature']
        humid = home['humid']
        distance_door = home['distance_door']
        distance_private_room = home['distance_private_room']
        update_home.delay(id, temperature, humid, distance_door, distance_private_room)
    except:
        pass
    






client = mqtt_client.Client()
client.username_pw_set(config('USERNAME_MQTT'), config('PASSWORD_MQTT'))
client.on_connect = on_connect
client.on_message = on_message
client.connect('mqtt.ngoinhaiot.com',1111)



