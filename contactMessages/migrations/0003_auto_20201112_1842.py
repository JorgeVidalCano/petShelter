# Generated by Django 3.1.2 on 2020-11-12 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contactMessages', '0002_auto_20201112_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manager_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
