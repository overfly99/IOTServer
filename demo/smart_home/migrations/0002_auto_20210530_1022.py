# Generated by Django 3.2.3 on 2021-05-30 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
                ('temperature', models.IntegerField(blank=True, default=25, null=True)),
                ('humid', models.IntegerField(blank=True, null=True)),
                ('distance_door', models.IntegerField(blank=True, null=True)),
                ('distance_private_room', models.IntegerField(blank=True, null=True)),
                ('host_mqtt', models.CharField(blank=True, max_length=100, null=True)),
                ('port_mqtt', models.CharField(blank=True, max_length=10, null=True)),
                ('topic', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Home',
                'verbose_name_plural': 'Homes',
            },
        ),
        migrations.AddField(
            model_name='devide',
            name='max_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devide',
            name='min_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devide',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smart_home.home'),
        ),
        migrations.DeleteModel(
            name='House',
        ),
    ]
