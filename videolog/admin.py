# -*- coding: utf-8 -*-
from django.contrib import admin
# utils:
from django.db.models import Q
from django.contrib.auth import get_user_model
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.extensions import PageExtensionAdmin
# models:
from .models import (VideoEntry, VideoPeople, VideoKeywords, VideoCategory,HeaderExtension)

class VideoCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    list_display = ('title', 'subtitle', 'slug')
    list_filter = ('sites',)

class VideoPeopleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}

class VideoKeywordsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}

class VideoEntryAdmin(PlaceholderAdminMixin, admin.ModelAdmin):
    readonly_fields = (
         'slug',
         'published_timestamp',
    )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = get_user_model().objects.filter(
                Q(is_superuser=True) | Q(user_permissions__content_type__app_label='videolog',
                user_permissions__content_type__model='entry')).distinct()
            kwargs['initial'] = request.user.id
        return super(VideoEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class HeaderExtensionAdmin(PageExtensionAdmin):
	pass

admin.site.register(VideoCategory, VideoCategoryAdmin)
admin.site.register(VideoPeople, VideoPeopleAdmin)
admin.site.register(VideoKeywords, VideoKeywordsAdmin)
admin.site.register(VideoEntry, VideoEntryAdmin)
admin.site.register(HeaderExtension, HeaderExtensionAdmin)
