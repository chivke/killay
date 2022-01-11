# Generated by Django 3.0.10 on 2021-09-20 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videocategorization',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='videos.VideoCollection', verbose_name='Collection'),
        ),
    ]