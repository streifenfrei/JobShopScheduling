# Generated by Django 3.0.7 on 2020-06-11 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='result_date',
        ),
        migrations.AlterField(
            model_name='result',
            name='result_image',
            field=models.CharField(max_length=255),
        ),
    ]