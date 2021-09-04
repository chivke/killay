# Generated by Django 3.0.10 on 2021-09-03 15:33

from django.db import migrations
from django.conf import settings


def create_initial_page_home(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID, defaults={"name": settings.SITE_NAME, "domain": settings.SITE_DOMAIN}
    )
    Page = apps.get_model("pages", "Page")
    Page.objects.update_or_create(
        slug="home", defaults={"title": settings.SITE_NAME}
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_page_home),
    ]
