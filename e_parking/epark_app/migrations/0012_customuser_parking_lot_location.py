# Generated by Django 4.2.4 on 2023-08-18 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epark_app', '0011_slotbooking_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='parking_lot_location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='epark_app.location'),
            preserve_default=False,
        ),
    ]