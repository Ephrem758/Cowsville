# Generated by Django 5.1 on 2024-10-25 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_farm_farm_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='fertility_window_end',
        ),
        migrations.RemoveField(
            model_name='animal',
            name='fertility_window_start',
        ),
        migrations.AddField(
            model_name='animal',
            name='last_heat_sign',
            field=models.DateField(blank=True, null=True),
        ),
    ]
