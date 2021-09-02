from django.contrib.auth.mixins import AccessMixin

from cmpirque.admin.models import SiteConfiguration


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PublishRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        conf = SiteConfiguration.objects.current()
        if not conf.is_published and not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
