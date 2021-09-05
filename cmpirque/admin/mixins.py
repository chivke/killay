from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, ListView, UpdateView
from django.urls import reverse
from django.utils.translation import gettext

from cmpirque.admin.models import SiteConfiguration
from cmpirque.videos.models import Video
from cmpirque.videos.forms import VideoForm, VideoMetaForm, VideoProviderFormSet


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
    template_name = "admin/generic_list.html"
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
    template_name = "admin/generic_form.html"
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
    template_name = "admin/generic_delete.html"
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


class VideoAdminMixin(AdminRequiredMixin):
    model = Video
    slug_field = "code"
    form_class = VideoForm
    meta_form_class = VideoMetaForm
    providers_formset_class = VideoProviderFormSet

    def get_meta_form(self):
        kwargs = super().get_form_kwargs()
        if self.object is not None:
            kwargs["instance"] = self.object.meta
        return self.meta_form_class(**kwargs)

    def get_providers_formset(self):
        kwargs = super().get_form_kwargs()
        if self.object is not None:
            kwargs["instance"] = self.object
        return self.providers_formset_class(**kwargs)

    def get_success_url(self):
        return reverse("admin:videos_update", kwargs={"slug": self.object.code})

    def validate_forms(self):
        form = self.get_form()
        meta_form = self.get_meta_form()
        providers_formset = self.get_providers_formset()
        if form.is_valid() and meta_form.is_valid() and providers_formset.is_valid():
            return self.form_valid(form, meta_form, providers_formset)
        else:
            return self.form_invalid(form, meta_form, providers_formset)

    def form_invalid(self, form, meta_form, providers_formset):
        context = self.get_context_data(form=form)
        context["meta_form"] = meta_form
        context["providers_formset"] = providers_formset
        messages.error(self.request, gettext("Error saving Video"))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        has_video = hasattr(self, "object") and getattr(self, "object") is not None
        context["meta_form"] = self.meta_form_class(
            **{"instance": self.object.meta} if has_video else {}
        )
        context["providers_formset"] = self.providers_formset_class(
            **{"instance": self.object} if has_video else {}
        )
        return context


class FormSetListMixin(AdminRequiredMixin, ListView):
    paginate_by = 50
    model = None
    formset_class = None
    label_plural = None
    reverse_url = None
    formset_title = None
    template_name = "admin/formset_list.html"

    def get_context_data(self, **kwargs):
        kwargs["total_of_objects"] = self.total_of_objects
        kwargs["formset_title"] = self.formset_title
        kwargs["label_plural"] = self.label_plural
        kwargs["query_search"] = self.query_search
        context = super().get_context_data()
        if "formset" not in kwargs and "object_list" in context:
            kwargs["formset"] = self.formset_class(queryset=context["object_list"])
        return {**context, **kwargs}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = self.formset_class(queryset=self.object_list, data=request.POST)
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def get_queryset(self):
        self.query_search = self.request.GET.get("q") or self.request.POST.get(
            "query_search"
        )
        queryset = (
            self.model.objects.all()
            if not self.query_search
            else self.model.objects.filter(name__icontains=self.query_search)
        )
        self.total_of_objects = queryset.count()
        return queryset

    def get_success_url(self):
        url = reverse(self.reverse_url) + "?"
        if self.query_search:
            url += f"q={self.query_search}"
        page_number = self.request.POST.get("page_number")
        if str(page_number).isnumeric():
            if url[-1] != "?":
                url += "&"
            url += f"page={page_number}"
        return url

    def formset_valid(self, formset):
        self.object_list = formset.save()
        messages.info(
            self.request, gettext(f"Video {self.label_plural} saved successfully")
        )
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        messages.error(self.request, gettext(f"Error saving video {self.label_plural}"))
        return self.render_to_response(context)
