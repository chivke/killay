# Generated by Django 3.2.21 on 2023-12-01 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20230828_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='collection_site',
        ),
    ]
