from rest_framework.serializers import ModelSerializer, Serializer
from smart_home.models import *
from rest_framework import serializers

class DevideSerilizer(ModelSerializer):
     
    class Meta:
        model = Device
        exclude = ['esp']


class EspSerializer(serializers.ModelSerializer):
    list_device = DevideSerilizer(many = True)

    class Meta:
        model = Esp
        fields = '__all__'

class HomeSerializer(ModelSerializer):
    list_esp = EspSerializer(many = True)

    class Meta:
        model = Home
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 255, required = True)
    password = serializers.CharField(max_length = 255, required = True, write_only = True)