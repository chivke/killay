# Generated by Django 3.2.18 on 2023-05-24 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provider',
            options={'ordering': ['plyr_provider'], 'verbose_name': 'video provider', 'verbose_name_plural': 'video provider'},
        ),
        migrations.AddField(
            model_name='category',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='archives.archive'),
        ),
        migrations.AddField(
            model_name='collection',
            name='is_restricted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='piece',
            name='is_restricted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='provider',
            name='file',
            field=models.FileField(null=True, upload_to='piece_files', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='provider',
            name='image',
            field=models.ImageField(null=True, upload_to='piece_images', verbose_name='Image'),
        ),
    ]
