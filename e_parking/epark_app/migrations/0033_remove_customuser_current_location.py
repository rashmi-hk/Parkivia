# Generated by Django 4.2.4 on 2023-09-04 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('epark_app', '0032_customuser_current_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='current_location',
        ),
    ]
