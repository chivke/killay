from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from filer.fields.file import FilerFileField
from django.db import models


class HeaderExtension(PageExtension):
    header_image = models.FileField(
        help_text="Page header image/ imagen de cabecera para página ",
        #related_name="header_image_headerextension",
        blank=True,
        null=True,
        )

extension_pool.register(HeaderExtension)
