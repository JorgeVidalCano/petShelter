# Generated by Django 3.1.2 on 2020-11-16 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactMessages', '0008_auto_20201115_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
    ]
