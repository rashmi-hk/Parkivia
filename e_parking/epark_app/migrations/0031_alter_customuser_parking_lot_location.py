# Generated by Django 4.2.4 on 2023-09-04 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epark_app', '0030_alter_openinghours_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='parking_lot_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='epark_app.location'),
        ),
    ]