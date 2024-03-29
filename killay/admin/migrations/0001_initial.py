# Generated by Django 3.0.10 on 2021-09-17 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Killay Site Name', max_length=250, verbose_name='Name of Site')),
                ('domain', models.CharField(default='killay-site.com', max_length=250, verbose_name='Domain')),
                ('is_published', models.BooleanField(default=True, verbose_name='Is published')),
                ('footer_is_visible', models.BooleanField(default=True, verbose_name='Footer is visible')),
                ('site', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='configuration', to='sites.Site')),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('youtube', 'Youtube'), ('vimeo', 'Vimeo')], max_length=150, verbose_name='Provider')),
                ('url', models.URLField(verbose_name='URL')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Is visible')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Position')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_medias', to='admin.SiteConfiguration')),
            ],
            options={
                'verbose_name': 'social media',
                'verbose_name_plural': 'social medias',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('image', models.ImageField(upload_to='logos', verbose_name='Image')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Is visible')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Position')),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logos', to='admin.SiteConfiguration')),
            ],
            options={
                'verbose_name': 'logo',
                'verbose_name_plural': 'logos',
                'ordering': ['position'],
            },
        ),
    ]
