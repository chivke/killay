from django.views.generic import DetailView
from django.shortcuts import redirect

from killay.pages.lib.constants import PageConstants
from killay.pages.models import Page

from killay.admin.views.mixins import PublishRequiredMixin


class PageDetailView(PublishRequiredMixin, DetailView):
    model = Page
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.object.kind == PageConstants.KIND_LINK and self.object.redirect_to:
            return redirect(self.object.redirect_to)
        return response

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        page = context["object"]
        menu_cursor = {
            "archive": page.collection.archive if page.collection else page.archive,
            "collection": page.collection,
            "type": "page",
        }
        self.request.menu_cursor = menu_cursor
        return context


page_detail_view = PageDetailView.as_view()
