from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy

from killay.admin.mixins import (
    AdminDeleteMixin,
    AdminListMixin,
    AdminRequiredMixin,
    AdminUpdateMixin,
)
from killay.pages.models import Page
from killay.pages.forms import PageForm
from django.utils.translation import gettext, gettext_lazy


class PageCreateView(AdminRequiredMixin, CreateView):
    form_class = PageForm
    template_name = "admin/generic_form.html"
    extra_context = {"form_title": gettext_lazy("Create Page")}
    html_fields = ["body"]

    def get_success_url(self):
        messages.info(self.request, gettext(f'Page "{self.object.title}" was created'))
        return reverse("admin:pages_update", kwargs={"slug": self.object.slug})


page_create_view = PageCreateView.as_view()


class PageUpdateView(AdminUpdateMixin):
    model = Page
    form_class = PageForm
    read_only_fields = ["created_at", "updated_at"]
    reverse_success_url = "admin:pages_update"


page_update_view = PageUpdateView.as_view()


class PageListView(AdminListMixin):
    model = Page
    list_fields = [
        "title",
        "slug",
        "is_visible",
        "is_visible_in_navbar",
        "is_visible_in_footer",
    ]
    list_title = gettext_lazy("Pages Administration")
    action_links = {
        "create_object": {
            "name": gettext_lazy("Create"),
            "link": reverse_lazy("admin:pages_create"),
        }
    }
    object_action_links = {
        "update_object": {"name": gettext_lazy("Update"), "link": "admin:pages_update"},
        "delete_object": {"name": gettext_lazy("Delete"), "link": "admin:pages_delete"},
    }


page_list_view = PageListView.as_view()


class PageDeleteView(AdminDeleteMixin):
    model = Page
    reverse_success_url = "admin:pages_list"


page_delete_view = PageDeleteView.as_view()
