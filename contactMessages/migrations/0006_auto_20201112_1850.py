# Generated by Django 3.1.2 on 2020-11-12 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactMessages', '0005_auto_20201112_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='manager',
            new_name='receiver',
        ),
    ]
