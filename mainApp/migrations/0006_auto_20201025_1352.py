# Generated by Django 3.1.2 on 2020-10-25 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_shelter_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelter',
            name='image',
            field=models.ImageField(default='default_shelter.jpg', upload_to='shelter_imagen'),
        ),
    ]