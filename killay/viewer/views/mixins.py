from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from killay.viewer.lib.constants import ViewerMessageConstants
from killay.viewer.engine.pipelines import RoutePipeline


class ViewerViewBase(TemplateView):
    out_of_scope = []

    @property
    def menu_cursor(self):
        if not hasattr(self.request, "menu_cursor"):
            self.request.menu_cursor = {}
        return self.request.menu_cursor

    @menu_cursor.setter
    def menu_cursor(self, value):
        self.request.menu_cursor = value

    def dispatch(self, request, *args, **kwargs):
        if request.viewer.scope in self.out_of_scope:
            if not request.user.is_superuser:
                url = RoutePipeline.get_root_url(request=self.request)
                return HttpResponseRedirect(redirect_to=url)
            message = ViewerMessageConstants.VIEW_OUT_OF_SCOPE.format(
                scope=request.viewer.scope
            )
            messages.warning(request, message)
        self.menu_cursor = {}
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs) -> dict:
        self.fetch_data()
        context = super().get_context_data(*args, **kwargs)
        view_context = self.get_view_context_data()
        context.update(view_context)
        return context

    def fetch_data(self) -> None:
        return

    def get_view_context_data(self) -> dict:
        return {}
