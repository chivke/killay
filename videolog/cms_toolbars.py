from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from videolog.models import (VideoEntry, HeaderExtension, VideoCategory, VideoPeople, VideoKeywords)

class VideoEntryToolbar(CMSToolbar):
    supported_apps = (
        'videolog',
    )
    watch_models = [VideoEntry,VideoCategory, VideoPeople, VideoKeywords]
    
    def populate(self):
        if not self.is_current_app:
            return
        menu = self.toolbar.get_or_create_menu('entry-app', _('Videos'))
        menu.add_sideframe_item(
            name=_('Lista de Videos'),
            url=admin_reverse('videolog_videoentry_changelist'),
        )
        menu.add_modal_item(
            name=_('Agregar Video'),
            url=admin_reverse('videolog_videoentry_add'),
        )
        menu.add_sideframe_item(
            name=_('Lista de categorías'),
            url=admin_reverse('videolog_videocategory_changelist'),
        )
        menu.add_modal_item(
            name=_('Agregar categoría'),
            url=admin_reverse('videolog_videocategory_add'),
        )
        menu.add_sideframe_item(
            name=_('Lista de personas'),
            url=admin_reverse('videolog_videopeople_changelist'),
        )
        menu.add_modal_item(
            name=_('Agregar persona'),
            url=admin_reverse('videolog_videopeople_add'),
        )
        menu.add_sideframe_item(
            name=_('Lista de keywords'),
            url=admin_reverse('videolog_videokeywords_changelist'),
        )
        menu.add_modal_item(
            name=_('Agregar keyword'),
            url=admin_reverse('videolog_videokeywords_add'),
        )

class HeaderExtensionToolbar(ExtensionToolbar):
    model = HeaderExtension
    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            page_extension, url = self.get_page_extension_admin()
            if url:
                current_page_menu.add_modal_item(_('Page Header'), url=url,
                    disabled=not self.toolbar.edit_mode_active, position=0)

toolbar_pool.register(VideoEntryToolbar)  # register the toolbar
toolbar_pool.register(HeaderExtensionToolbar)
