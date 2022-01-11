# Generated by Django 3.0.10 on 2021-08-27 03:52

from django.db import migrations
from django.conf import settings


def create_initial_adminconfig(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    SiteConfiguration = apps.get_model("admin", "SiteConfiguration")
    Site.objects.update_or_create(
        id=settings.SITE_ID, defaults={"name": settings.SITE_NAME, "domain": settings.SITE_DOMAIN}
    )
    SiteConfiguration.objects.update_or_create(id=settings.SITE_ID)


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_adminconfig),
    ]