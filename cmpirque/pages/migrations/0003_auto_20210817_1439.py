# Generated by Django 3.0.10 on 2021-08-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='page',
            name='is_visible_on_menu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='page',
            name='with_header_image',
            field=models.BooleanField(default=True),
        ),
    ]
