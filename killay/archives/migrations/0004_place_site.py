# Generated by Django 3.2.18 on 2023-05-26 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('archives', '0003_place_placeaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='places', to='sites.site'),
        ),
    ]
