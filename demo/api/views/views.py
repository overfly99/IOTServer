from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from api.serializers import *
from django.shortcuts import get_object_or_404
from smart_home.models import *
from paho.mqtt import client as mqtt_client
import json
from drf_yasg.utils import swagger_auto_schema
from smart_home.tasks import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class HomeAPI(ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]

    def list(self,request):
        homes = Home.objects.filter(user =request.user)
        serializer = HomeSerializer(homes, many = True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        queryset = Home.objects.all()
        home = get_object_or_404(queryset, pk = pk)
        serializer = HomeSerializer(home)
        return Response(serializer.data)
    
    def update(self,request,pk):
        home = Home.objects.get(pk = pk)
        serializer = HomeSerializer(home,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DeviceAPI(ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    def list(self,request):
        devices = Device.objects.all()
        serializer = DevideSerilizer(devices, many = True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        device = Device.objects.get(pk = pk)
        serializer = DevideSerilizer(device)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = DevideSerilizer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status =status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        device = Device.objects.get(pk = pk)
        serializer = DevideSerilizer(device,data = request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['auto'] == 'ON':
                msg = json.dumps({'pin':serializer.data['pin_number'], 'status':serializer.data['status']})
                pub.delay(device.esp.host_mqtt, device.esp.port_mqtt,device.esp.topic,msg)
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

# class DeviceAPIview(GenericAPIView):
#     serializer_class = DevideSerilizer

#     def get(self,request):
#         devices = Device.objects.all()
#         serializer = DevideSerilizer(devices, many =True)
#         return Response(serializer.data)


#     def post(self,request):
#         serializer = DevideSerilizer(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status = status.HTTP_201_CREATED)     

class EspAPI(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    queryset = Esp.objects.all()
    serializer_class = EspSerializer
    # def list(self,request):
    #     esps = Esp.objects.all()
    #     serializer = EspSerializer(esps ,many = True)
    #     return Response(serializer.data)

    # def retrieve(self,request,pk):
    #     try:
    #         esp = Esp.objects.get(pk = pk)
    #         serializer = EspSerializer(esp)
    #         return Response(serializer.data)
    #     except Esp.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

class LoginAPI(APIView):
    permission_classes = ()
    authentication_classes = []

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = request.data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                try:
                    token = Token.objects.get(user = user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user = user)
                return Response({'token':token.key}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'username or password not valid'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                   
    