# Generated by Django 4.1.1 on 2022-09-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0044_alter_departures_date_alter_payments_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departures',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='refunds',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата'),
        ),
    ]