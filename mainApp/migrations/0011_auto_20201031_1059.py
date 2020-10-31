# Generated by Django 3.1.2 on 2020-10-31 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0010_auto_20201031_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelter',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]