from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from .cms_menus import CategoryMenu

class VideoLogApphook(CMSApp):
    app_name = "videolog"
    name = _("Video Log")
    def get_urls(self, page=None, language=None, **kwargs):
        return ["videolog.urls"]

apphook_pool.register(VideoLogApphook)  # register the application