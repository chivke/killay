from django.db import migrations


def create_initial_viewer_data(apps, schema_editor):
    Viewer = apps.get_model("viewer", "Viewer")
    SiteConfiguration = apps.get_model("admin", "SiteConfiguration")

    site_configurations = SiteConfiguration.objects.all()
    for conf in site_configurations:
        Viewer.objects.get_or_create(configuration_id=conf.id)


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_viewer_data),
    ]
