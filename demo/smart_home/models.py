from enum import auto
from typing import no_type_check
from django.db import models
from django.db.models.base import Model  
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _ 
# Create your models



class Home(models.Model):
    """Model definition for House."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for House."""

        verbose_name = 'Home'
        verbose_name_plural = 'Homes'
    name = models.CharField(null = True, blank =False, max_length=50, unique=True)
    temperature = models.FloatField(default = 25, null = True, blank=True)
    humid = models.FloatField(null=True, blank=True)
    distance_door = models.FloatField(null=True,blank=True)
    distance_private_room = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        """Unicode representation of House."""
        return self.name
    
    def get_info(self):
        return {'temperature':self.temperature, 'humid':self.humid, 'distance_door':self.distance_door, 'distance_private_room':self.distance_private_room}

class Type(models.Model):
    name = models.CharField(max_length=50, null=False,blank=False, unique=True)

    def __str__(self):
        return self.name



class Esp(models.Model):
    class Meta:
        db_table = 'Esp'
        verbose_name = _("ESP")
        verbose_name_plural = _('ESP')
    
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null=True, blank=True, related_name='list_esp')
    name = models.CharField(max_length=100)
    host_mqtt = models.CharField(null=True, blank=True,max_length=100)
    port_mqtt = models.CharField(null=True, blank=True, max_length=10)
    topic = models.CharField(null=True, blank=True,max_length=100)

    def __str__(self):
        return '{}'.format(self.pk)

class Device(models.Model):
    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    status_choice = [
        ('ON', "ON"),
        ('OFF','OFF')
    ]
    name = models.CharField(max_length=50,null=False, blank=False)
    type = models.ForeignKey('smart_home.Type', on_delete=models.CASCADE, null=False,blank=False)
    status = models.CharField(_('Status'), choices=status_choice, null=True, blank=True, max_length = 10)
    auto = models.CharField(_('Auto'),choices=status_choice,null=True,blank=True, max_length = 10)
    esp = models.ForeignKey(Esp, on_delete=models.CASCADE, null=True, blank=True, related_name = 'list_device')
    pin_number = models.IntegerField(unique=True, null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    min_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name