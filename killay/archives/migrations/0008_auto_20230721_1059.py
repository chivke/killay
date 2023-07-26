# Generated by Django 3.2.18 on 2023-07-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0007_alter_piece_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='image',
            field=models.ImageField(null=True, upload_to='archive_images', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='collection',
            name='image',
            field=models.ImageField(null=True, upload_to='collection_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='file',
            field=models.FileField(null=True, upload_to='piece_files', verbose_name='File'),
        ),
    ]