# Generated by Django 4.1.7 on 2023-05-29 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_remove_session_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coordinate',
        ),
    ]
