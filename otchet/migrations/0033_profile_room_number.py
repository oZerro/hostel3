# Generated by Django 4.1.1 on 2022-09-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0032_delete_nikola'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='room_number',
            field=models.CharField(default='', max_length=2, verbose_name='Номер комнаты'),
        ),
    ]
