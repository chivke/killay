from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from filer.fields.file import FilerFileField

class HeaderExtension(PageExtension):
    header_image = FilerFileField(
        help_text="Page header image/ imagen de cabecera para página ",
        related_name="header_image_headerextension",
        blank=True,
        null=True,
        )
    subheader_image = FilerFileField(
        help_text="Page subheader image/ imagen de subcabecera para página ",
        related_name="subheader_image_headerextension",
        blank=True,
        null=True,
        )

extension_pool.register(HeaderExtension)
