# Generated by Django 4.2.5 on 2024-02-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Niwi_Travels', '0002_passenger_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='children',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]