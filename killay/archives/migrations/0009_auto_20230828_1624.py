# Generated by Django 3.2.20 on 2023-08-28 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0008_auto_20230721_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placeaddress',
            options={'ordering': ['ipv4'], 'verbose_name': 'place address', 'verbose_name_plural': 'place addresses'},
        ),
        migrations.AlterModelOptions(
            name='provider',
            options={'ordering': ['active'], 'verbose_name': 'provider', 'verbose_name_plural': 'providers'},
        ),
        migrations.AlterField(
            model_name='archive',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the archive', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='archive',
            name='image',
            field=models.ImageField(help_text='Representative image of the archive', null=True, upload_to='archive_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='archive',
            name='is_restricted',
            field=models.BooleanField(default=False, help_text='Indicates if the archive will be restricted to some public', verbose_name='Is restricted'),
        ),
        migrations.AlterField(
            model_name='archive',
            name='is_visible',
            field=models.BooleanField(default=True, help_text='Indicates if the archive will be visible to the public', verbose_name='Is visible'),
        ),
        migrations.AlterField(
            model_name='archive',
            name='name',
            field=models.CharField(help_text='Name of the Archive', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='archive',
            name='position',
            field=models.PositiveSmallIntegerField(default=0, help_text='Determines the position in which it will be displayed, the smaller the number, the earlier it will be located', verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='archive',
            name='slug',
            field=models.SlugField(help_text='Slug of the archive, must be unique in the site', max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='collection',
            field=models.ForeignKey(help_text='Collection to which the category belongs', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='archives.collection', verbose_name='Collection'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='archive',
            field=models.ForeignKey(help_text='Archive to which the collection belongs', on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='archives.archive', verbose_name='Archive'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(help_text='Representative image of the collection', null=True, upload_to='collection_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='is_restricted',
            field=models.BooleanField(default=False, help_text='Indicates if the collection will be restricted to some public', verbose_name='Is restricted'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='is_visible',
            field=models.BooleanField(default=True, help_text='Indicates if the collection will be visible to the public', verbose_name='Is visible'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='categories',
            field=models.ManyToManyField(help_text='Categories to which the piece belongs', related_name='pieces', to='archives.Category', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='code',
            field=models.SlugField(help_text='Code of the piece, must be unique in the site', verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='collection',
            field=models.ForeignKey(help_text='Collection to which the piece belongs', on_delete=django.db.models.deletion.CASCADE, related_name='pieces', to='archives.collection', verbose_name='Collection'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='is_published',
            field=models.BooleanField(default=False, help_text='If the piece is not published, you will need to log in as admin to visit it', verbose_name='Is published'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='is_restricted',
            field=models.BooleanField(default=False, help_text='Indicates if the piece will be restricted to some public', verbose_name='Is restricted'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='keywords',
            field=models.ManyToManyField(help_text='Keywords related to the piece', related_name='pieces', to='archives.Keyword', verbose_name='Keywords'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='kind',
            field=models.CharField(choices=[('VIDEO', 'Video'), ('IMAGE', 'Image'), ('SOUND', 'Sound'), ('DOCUMENT', 'Document')], help_text='Kind of the piece (video, sound, image or document)', max_length=50, verbose_name='Kind'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='people',
            field=models.ManyToManyField(help_text='People who relate to the piece', related_name='pieces', to='archives.Person', verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='thumb',
            field=models.ImageField(blank=True, help_text='thumbnail of representative image of the piece', null=True, upload_to='piece_thumbs', verbose_name='Thumb'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='title',
            field=models.CharField(help_text='Title of the piece', max_length=512, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='archivist_notes',
            field=models.TextField(blank=True, help_text='Archivist notes of the piece', null=True, verbose_name='Archivist Notes'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the piece', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='description_date',
            field=models.DateField(blank=True, help_text='Date of the description', null=True, verbose_name='Description Date'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='documentary_unit',
            field=models.CharField(blank=True, help_text='Documentary unit of the piece', max_length=500, null=True, verbose_name='Documentary Unit'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='duration',
            field=models.TimeField(blank=True, help_text='Piece duration if applicable', null=True, verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='event',
            field=models.CharField(blank=True, help_text='Event related to the piece', max_length=500, null=True, verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='lang',
            field=models.CharField(blank=True, help_text='Language of the piece', max_length=500, null=True, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='location',
            field=models.CharField(blank=True, help_text='Location related to the piece', max_length=500, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='notes',
            field=models.TextField(blank=True, help_text='Notes related to the piece', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='original_format',
            field=models.CharField(blank=True, help_text='Original format of the piece', max_length=500, null=True, verbose_name='Original Format'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='productor',
            field=models.CharField(blank=True, help_text='Productor of the piece', max_length=500, null=True, verbose_name='Productor'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='register_author',
            field=models.CharField(blank=True, help_text='Author of the piece record', max_length=500, null=True, verbose_name='Register Author'),
        ),
        migrations.AlterField(
            model_name='piecemeta',
            name='register_date',
            field=models.DateField(blank=True, help_text='Register date of the piece', null=True, verbose_name='Register Date'),
        ),
        migrations.AlterField(
            model_name='place',
            name='allowed_archives',
            field=models.ManyToManyField(help_text='Restricted archives that are allowed to see from the place', related_name='allowed_places', to='archives.Archive', verbose_name='Allowed Archives'),
        ),
        migrations.AlterField(
            model_name='place',
            name='allowed_collections',
            field=models.ManyToManyField(help_text='Restricted collections that are allowed to see from the place', related_name='allowed_places', to='archives.Collection', verbose_name='Allowed Collections'),
        ),
        migrations.AlterField(
            model_name='place',
            name='allowed_pieces',
            field=models.ManyToManyField(help_text='Restricted pieces that are allowed to see from the place', related_name='allowed_places', to='archives.Piece', verbose_name='Allowed Pieces'),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(help_text='Name of the place', max_length=500, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='placeaddress',
            name='description',
            field=models.CharField(blank=True, help_text='Description of the place address', max_length=500, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='placeaddress',
            name='ipv4',
            field=models.GenericIPAddressField(db_index=True, help_text='IP Address of the place', unique=True, verbose_name='IP Address'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='active',
            field=models.BooleanField(default=False, help_text='Determines if the provider is active, only one provider can be active at a time', verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='checked_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Online Checked At'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='file',
            field=models.FileField(help_text='File hosted on the server, field used by pieces of kind document and sound', null=True, upload_to='piece_files', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='image',
            field=models.ImageField(help_text='Image hosted on the server, field used by pieces of kind image', null=True, upload_to='piece_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='ply_embed_id',
            field=models.CharField(help_text='Video ID to be embedded in the player, field used by pieces of kind video', max_length=500, verbose_name='Video Embed ID'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='plyr_provider',
            field=models.CharField(choices=[('youtube', 'Youtube'), ('vimeo', 'Vimeo')], help_text='Video provider associated with the embed ID, field used by pieces of kind video', max_length=50, verbose_name='Video Provider'),
        ),
        migrations.AlterField(
            model_name='sequence',
            name='content',
            field=models.TextField(blank=True, help_text='Tex content of piece sequence', null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='sequence',
            name='end',
            field=models.TimeField(help_text='End time of piece sequence', verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='sequence',
            name='ini',
            field=models.TimeField(help_text='Initiation time of piece sequence', verbose_name='Initiation'),
        ),
        migrations.AlterField(
            model_name='sequence',
            name='title',
            field=models.CharField(blank=True, help_text='Title of piece sequence', max_length=500, null=True, verbose_name='Title'),
        ),
    ]
