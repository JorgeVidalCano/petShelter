# Generated by Django 3.1.2 on 2020-10-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20201025_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelter',
            name='about',
            field=models.CharField(default='Add something about your shelter', max_length=300),
        ),
    ]
