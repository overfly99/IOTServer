# Generated by Django 3.2.5 on 2021-07-20 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home', '0006_auto_20210712_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='home',
        ),
    ]
