# Generated by Django 3.0.7 on 2020-06-28 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sa', '0005_auto_20200627_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='count_increase',
            field=models.FloatField(default=1.2),
        ),
    ]
