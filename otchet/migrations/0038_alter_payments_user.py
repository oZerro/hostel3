# Generated by Django 4.1.1 on 2022-09-14 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0037_alter_payments_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='otchet.profile', verbose_name='Профиль'),
        ),
    ]
