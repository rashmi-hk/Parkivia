# Generated by Django 4.2.4 on 2023-08-18 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('epark_app', '0014_remove_slotdetail_available_slots_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotbooking',
            name='vehicle_type',
        ),
    ]
