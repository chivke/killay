# Generated by Django 3.0.10 on 2021-09-03 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('admin', '0002_add_initial_admin_configuration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('slug', models.SlugField(max_length=150, verbose_name='Slug')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Body')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Is visible')),
                ('is_visible_in_navbar', models.BooleanField(default=False, verbose_name='Is visible in navbar')),
                ('is_visible_in_footer', models.BooleanField(default=False, verbose_name='Is visible in footer')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='page_images', verbose_name='Header mage')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('site', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='sites.Site')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
                'unique_together': {('slug', 'site')},
            },
        ),
    ]
