# Generated by Django 3.1.2 on 2020-10-19 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20201019_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='features',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atributos', to='mainApp.feature'),
        ),
    ]
