from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import VideoEntryPluginModel
from django.utils.translation import ugettext as _
from django.views.generic import ListView

@plugin_pool.register_plugin
class VideoEntryPluginPublisher(CMSPluginBase):
    model = VideoEntryPluginModel  # model where plugin data are saved
    name = _("Entry Video Plugin")  # name of the plugin in the interface
    render_template = "videolog/entry_plugin.html"
    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context
