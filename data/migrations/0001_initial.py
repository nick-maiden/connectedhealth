# Generated by Django 4.1.7 on 2023-03-17 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.FloatField(help_text='Enter the width (x value) for the coordinate: ')),
                ('height', models.FloatField(help_text='Enter the height (y value) for the coordinate: ')),
                ('depth', models.FloatField(help_text='Enter the depth (z value) for the coordinate: ')),
                ('frame', models.IntegerField(help_text='Enter the number of the frame corresponding to this coordinate: ')),
            ],
        ),
    ]
