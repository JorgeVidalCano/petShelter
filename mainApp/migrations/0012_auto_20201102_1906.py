# Generated by Django 3.1.2 on 2020-11-02 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_auto_20201031_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='features',
            field=models.ManyToManyField(blank=True, related_name='pet_atributos_many', to='mainApp.Feature'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='pet',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='pet_atributo', to='mainApp.pet'),
        ),
    ]
