# Generated by Django 4.2.4 on 2023-08-18 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epark_app', '0013_alter_customuser_parking_lot_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotdetail',
            name='available_slots',
        ),
        migrations.RemoveField(
            model_name='slotdetail',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='slotdetail',
            name='hourly_rate',
        ),
        migrations.RemoveField(
            model_name='slotdetail',
            name='vehicle_type',
        ),
        migrations.CreateModel(
            name='SlotDetailVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('available_slots', models.PositiveIntegerField(default=0)),
                ('vehicle_type', models.CharField(choices=[('2_wheeler', '2 Wheeler'), ('4_wheeler', '4 Wheeler'), ('Truck', 'Truck'), ('Bus', 'Bus'), ('Heavy Vehicle', 'Heavy Vehicle')], default='2_wheeler', max_length=20)),
                ('hourly_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epark_app.slotdetail')),
            ],
            options={
                'verbose_name_plural': 'Slot Detail Variants',
                'db_table': 'slotdetailvariant',
            },
        ),
        migrations.AddField(
            model_name='slotdetail',
            name='slot_variants',
            field=models.ManyToManyField(to='epark_app.slotdetailvariant'),
        ),
    ]