# Generated by Django 3.1.2 on 2020-10-24 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_auto_20201024_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='default',
            new_name='mainPic',
        ),
    ]
