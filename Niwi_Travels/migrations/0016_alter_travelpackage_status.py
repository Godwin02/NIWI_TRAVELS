# Generated by Django 4.2.5 on 2023-11-17 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Niwi_Travels', '0015_travelpackage_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelpackage',
            name='status',
            field=models.CharField(choices=[('Running', 'Running'), ('Paused', 'Paused')], default='Pending', max_length=10),
        ),
    ]
