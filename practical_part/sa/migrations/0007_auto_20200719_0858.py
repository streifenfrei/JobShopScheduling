# Generated by Django 3.0.7 on 2020-07-19 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sa', '0006_auto_20200628_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='lower_bound',
            field=models.CharField(default='K.a', max_length=255),
        ),
        migrations.AddField(
            model_name='table',
            name='upper_bound',
            field=models.CharField(default='K.a', max_length=255),
        ),
    ]