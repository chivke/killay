from django.views.generic import DetailView

from killay.pages.models import Page

from killay.admin.views.mixins import PublishRequiredMixin


class PageDetailView(PublishRequiredMixin, DetailView):
    model = Page
    slug_field = "slug"
    slug_url_kwarg = "slug"


page_detail_view = PageDetailView.as_view()
