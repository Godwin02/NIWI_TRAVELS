# Generated by Django 4.2.5 on 2023-11-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Niwi_Travels', '0014_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelpackage',
            name='feed',
            field=models.CharField(choices=[('Save', 'Save'), ('Post', 'Post')], default='Save', max_length=10),
        ),
    ]
