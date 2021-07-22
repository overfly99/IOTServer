from django.contrib import admin
from django.contrib.admin.decorators import register
from django.db.models import base
from django.contrib.auth.models import Group

# Register your models here.
from .models import *

class DevideAdminInline(admin.StackedInline):
    model = Device
    verbose_name = 'Devide'
    verbose_name_plural = 'Devides'

class ESPInline(admin.StackedInline):
    model = Esp
    verbose_name = "Esp"
    verbose_name_plural = "Esps"


class HomeAdmin(admin.ModelAdmin):
    list_display = ['name', 'temperature', 'humid','distance_door', 'distance_private_room']
    inlines = [ESPInline]

class EspAdmin(admin.ModelAdmin):
    inlines = [DevideAdminInline]
    list_display = ['name', 'host_mqtt','port_mqtt', 'topic']

admin.site.register(Home,HomeAdmin)
admin.site.register(Type)
admin.site.register(Esp,EspAdmin)
admin.site.register(Device)