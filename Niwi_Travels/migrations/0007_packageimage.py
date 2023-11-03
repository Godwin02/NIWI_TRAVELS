# Generated by Django 4.2.5 on 2023-10-31 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Niwi_Travels', '0006_remove_travelpackage_booking_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='package_images/')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Niwi_Travels.travelpackage')),
            ],
        ),
    ]
