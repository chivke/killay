
from django.views.generic import DetailView

from cmpirque.pages.models import Page


class PageDetailView(DetailView):
    model = Page
    slug_field = "slug"
    slug_url_kwarg = "slug"


page_detail_view = PageDetailView.as_view()
