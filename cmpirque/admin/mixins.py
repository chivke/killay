from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.views.generic import DeleteView, ListView, UpdateView
from django.urls import reverse
from cmpirque.admin.models import SiteConfiguration
from django.utils.translation import gettext


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


class AdminListMixin(AdminRequiredMixin, ListView):
    model = None
    template_name = "admin/components/generic_list.html"
    list_fields = []
    list_title = None
    action_links = {}
    object_action_links = {}
    slug_key = "slug"

    def get_object_list_values(self):
        object_list_values = [
            {
                **obj,
                "actions": {
                    action_name: {
                        **action,
                        "link": reverse(
                            action["link"], kwargs={"slug": obj[self.slug_key]}
                        ),
                    }
                    for action_name, action in self.object_action_links.items()
                },
            }
            for obj in self.object_list.values(*self.list_fields)
        ]
        return object_list_values

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["list_title"] = self.list_title
        context["list_fields"] = self.list_fields
        context["model_fields"] = self.model._meta.get_fields()
        context["object_list_values"] = self.get_object_list_values()
        context.update(self.action_links)
        return context


class AdminUpdateMixin(AdminRequiredMixin, UpdateView):
    model = None
    form_class = None
    template_name = "admin/components/generic_form.html"
    slug_field = "slug"
    read_only_fields = []
    reverse_success_url = None

    def get_success_url(self):
        message = gettext(
            f'{self.model._meta.verbose_name} "{self.object}" was updated'
        )
        messages.info(self.request, message)
        return reverse(
            self.reverse_success_url,
            kwargs={"slug": getattr(self.object, self.slug_field)},
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["read_only_fields"] = {
            field: {
                "value": value,
                "label": self.model._meta.get_field(field).verbose_name,
            }
            for field, value in self.object.__dict__.items()
            if field in self.read_only_fields
        }
        context["form_title"] = gettext(f"Update {self.object}")
        return context


class AdminDeleteMixin(AdminRequiredMixin, DeleteView):
    model = None
    template_name = "admin/components/generic_delete.html"
    reverse_success_url = None

    def get_success_url(self):
        message = gettext(
            f'{self.model._meta.verbose_name} "{self.object}" was deleted'
        )
        messages.warning(self.request, message)
        return reverse(self.reverse_success_url)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["delete_title"] = gettext(f"Delete {self.model._meta.verbose_name}")
        return context
