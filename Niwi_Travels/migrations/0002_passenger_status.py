# Generated by Django 4.2.5 on 2024-02-09 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Niwi_Travels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
