
from django.contrib import admin
from .models import HeaderExtension
from cms.extensions import PageExtensionAdmin


class HeaderExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(HeaderExtension, HeaderExtensionAdmin)
