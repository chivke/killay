# Generated by Django 3.2.20 on 2023-08-07 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0004_auto_20230504_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='domain',
            field=models.CharField(default='killay-site.com', help_text='Domain of the site (example.com)', max_length=250, verbose_name='Domain'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='footer_is_visible',
            field=models.BooleanField(default=True, help_text='Indicates whether or not the footer will be displayed', verbose_name='Footer is visible'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='is_published',
            field=models.BooleanField(default=True, help_text='If the site is not published, you will need to log in to visit it', verbose_name='Is published'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='name',
            field=models.CharField(default='Killay Site Name', help_text='Site name, can be omitted with certain display options', max_length=250, verbose_name='Name of Site'),
        ),
    ]
