# Generated by Django 3.2.18 on 2023-06-06 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0005_auto_20230529_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='archives.collection'),
        ),
    ]