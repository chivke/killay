from django.views.generic import DetailView, TemplateView

from cmpirque.pages.models import Page

from cmpirque.admin.mixins import PublishRequiredMixin


class PageDetailView(PublishRequiredMixin, DetailView):
    model = Page
    slug_field = "slug"
    slug_url_kwarg = "slug"


page_detail_view = PageDetailView.as_view()


class HomeView(PublishRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home_page"] = self.get_home_if_exists()
        return context

    def get_home_if_exists(self):
        return Page.objects.get(slug="home")


home_page_view = HomeView.as_view()
