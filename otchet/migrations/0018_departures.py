# Generated by Django 4.0.5 on 2022-09-10 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0017_profile_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='otchet.profile', verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Выезд',
                'verbose_name_plural': 'Выезды',
            },
        ),
    ]
