# Generated by Django 4.1.7 on 2023-03-23 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_coordinate_frame_user_delete_coordinates_frame_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(help_text='Enter date and time that this session started: ')),
            ],
        ),
        migrations.RemoveField(
            model_name='frame',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='frame',
            name='user',
        ),
        migrations.CreateModel(
            name='InvolvedInSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.ForeignKey(help_text='Enter the id of the session that this user participated in: ', on_delete=django.db.models.deletion.CASCADE, to='data.session')),
                ('user', models.ForeignKey(help_text='Enter the id of the user who participated in this session: ', on_delete=django.db.models.deletion.CASCADE, to='data.user')),
            ],
        ),
        migrations.AddField(
            model_name='frame',
            name='session',
            field=models.ForeignKey(default=1, help_text='Enter the id of the session that this frame belongs to: ', on_delete=django.db.models.deletion.CASCADE, to='data.session'),
            preserve_default=False,
        ),
    ]
