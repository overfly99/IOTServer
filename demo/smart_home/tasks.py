from __future__ import absolute_import, unicode_literals
from celery import shared_task
from paho.mqtt import client as mqtt_client
from decouple import config
from .models import *
import json

@shared_task
def pub(host:str, port:int, topic:str, msg:str):
    try:
        client = mqtt_client.Client()    
        client.username_pw_set(config('USERNAME_MQTT'), config('PASSWORD_MQTT'))
        client.connect(host, port)
        client.publish(topic, msg)
    except:
        pass

@shared_task
def update_home(id, temperature, humid, distance_door, distance_private_room):
    try:
        home = Home.objects.get(pk = id)
        home.temperature = temperature
        home.humid = humid
        home.distance_door = distance_door
        home.distance_private_room = distance_private_room
        home.save()
        device_list = Device.objects.filter(esp__home=home, auto='ON')
        info = home.get_info()
        for obj in device_list:
            try:
                value = info.get(obj.type.name)
                if (obj.min_value > value or obj.max_value <value):
                    if obj.status == 'OFF':
                        obj.status = 'ON'
                        obj.save()
                        msg = json.dumps({'pin':obj.pin_number, 'status':"ON"})
                        pub.delay(obj.esp.host_mqtt, int(obj.esp.port_mqtt), obj.esp.topic, msg)
                    else:
                        pass
                else:
                    if obj.status == 'ON':
                        obj.status = 'OFF'
                        obj.save()
                        msg = json.dumps({'pin':obj.pin_number, 'status':"OFF"})
                        pub.delay(obj.esp.host_mqtt, int(obj.esp.port_mqtt), obj.esp.topic, msg)
            except:
                pass

    except:
        pass
