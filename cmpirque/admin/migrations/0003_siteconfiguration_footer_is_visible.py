# Generated by Django 3.0.10 on 2021-09-03 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_add_initial_admin_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='footer_is_visible',
            field=models.BooleanField(default=True, verbose_name='Footer is visible'),
        ),
    ]