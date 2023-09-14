from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View, DeleteView, ListView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext

from killay.admin.models import SiteConfiguration
from killay.videos.models import Video
from killay.videos.forms import (
    VideoCategorizationForm,
    VideoForm,
    VideoMetaForm,
    VideoProviderFormSet,
)


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
        context["form_title"] = gettext(
            f"Update {self.object._meta.verbose_name} {self.object}"
        )
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
    categorization_form_class = VideoCategorizationForm

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

    def get_categorization_form(self):
        kwargs = super().get_form_kwargs()
        if self.object is not None:
            kwargs["instance"] = self.object.categorization
        return self.categorization_form_class(**kwargs)

    def get_success_url(self):
        return reverse(
            "admin:videos_update",
            kwargs={
                "collection": self.object.collection_slug,
                "slug": self.object.code,
            },
        )

    def validate_forms(self):
        form = self.get_form()
        meta_form = self.get_meta_form()
        categorization_form = self.get_categorization_form()
        providers_formset = self.get_providers_formset()
        if (
            form.is_valid()
            and meta_form.is_valid()
            and categorization_form.is_valid()
            and providers_formset.is_valid()
        ):
            return self.form_valid(
                form, meta_form, categorization_form, providers_formset
            )
        else:
            return self.form_invalid(
                form, meta_form, categorization_form, providers_formset
            )

    def form_invalid(self, form, meta_form, categorization_form, providers_formset):
        context = self.get_context_data(form=form)
        context["meta_form"] = meta_form
        context["providers_formset"] = providers_formset
        context["categorization_form"] = categorization_form
        messages.error(self.request, gettext("Error saving Video"))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        has_video = hasattr(self, "object") and getattr(self, "object") is not None
        context["meta_form"] = self.meta_form_class(
            **{"instance": self.object.meta} if has_video else {}
        )
        context["categorization_form"] = self.categorization_form_class(
            **{"instance": self.object.categorization} if has_video else {}
        )
        context["providers_formset"] = self.providers_formset_class(
            **{"instance": self.object} if has_video else {}
        )
        return context


class FormSetMixin(
    AdminRequiredMixin, MultipleObjectMixin, TemplateResponseMixin, View
):
    model = None
    slug_field = "slug"
    slug_url_field = "slug"
    formset_class = None
    search_field = "name"
    reverse_url = None
    title = None
    template_name = "admin/formset_list.html"
    paginate_by = 50
    compact_fields = []
    filters = None
    extra_context = {}
    filter_applied = {}

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.validate_formset(request=request)

    def get_queryset(self):
        queryset = self.model.objects.all()
        queryset = self.apply_filters(queryset)
        return queryset

    def apply_filters(self, queryset):
        queryset = self.set_search_filter_if_exists(queryset)
        queryset = self.set_custom_filter_if_exists(queryset)
        self.total_of_objects = queryset.count()
        page_size = self.get_paginate_by(queryset)
        self.pagination_context = {}
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size
            )
            self.pagination_context.update(
                {"paginator": paginator, "page_obj": page, "is_paginated": is_paginated}
            )
        else:
            self.pagination_context.update(
                {"paginator": paginator, "page_obj": page, "is_paginated": is_paginated}
            )
        self.pagination_context.update({"object_list": queryset})
        return queryset

    def set_search_filter_if_exists(self, queryset):
        self.query_search = self.request.GET.get("q") or self.request.POST.get(
            "query_search"
        )
        if self.query_search:
            queryset = queryset.filter(
                **{f"{self.search_field}__icontains": self.query_search}
            )
        return queryset

    def set_custom_filter_if_exists(self, queryset):
        if not self.filters:
            return queryset
        filters = {}
        for keyword, field in self.filters.items():
            value = self.request.GET.get(keyword) or self.request.POST.get(keyword)
            value = value.strip() if value else None
            if value:
                filters[field] = value
                self.filter_applied[keyword] = value
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = self.get_extra_context()
        if self.filters:
            context["filter_options"] = self.get_filter_options()
        context["total_of_objects"] = self.total_of_objects
        context["title"] = self.title
        context["query_search"] = self.query_search
        context["filter_applied"] = self.filter_applied
        context["model_name_plural"] = self.get_model_name_plural()
        context["compact_fields"] = self.compact_fields
        context.update(self.pagination_context)
        if self.create_reverse_link:
            context["create_link"] = self.get_create_link()
        if "formset" not in kwargs:
            kwargs["formset"] = self.formset_class(queryset=self.object_list)
        return {**context, **kwargs}

    def get_filter_options(self):
        return {}

    def get_create_link(self):
        return reverse(self.create_reverse_link)

    def validate_formset(self, request, **kwargs):
        formset = self.formset_class(
            queryset=self.object_list, data=request.POST, **kwargs
        )
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def get_success_url(self):
        url = reverse(self.reverse_url, kwargs=self.get_success_url_kwargs()) + "?"
        if self.query_search:
            url += f"q={self.query_search}"
        page_number = self.request.POST.get("page_number")
        if str(page_number).isnumeric():
            if url[-1] != "?":
                url += "&"
            url += f"page={page_number}"
        return url

    def formset_valid(self, formset):
        formset.save()
        messages.info(self.request, self.get_success_messange())
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        context = self.get_context_data(formset=formset)
        messages.error(self.request, self.get_error_menssage())
        return self.render_to_response(context)

    def get_extra_context(self):
        return self.extra_context or {}

    def get_success_url_kwargs(self):
        return {}

    def get_model_name_plural(self):
        return self.model._meta.verbose_name_plural

    def get_success_messange(self):
        return gettext(f"{self.model._meta.verbose_name_plural} saved successfully")

    def get_error_menssage(self):
        return gettext(f"Error saving {self.model._meta.verbose_name_plural}")


class InlineFormSetMixin(FormSetMixin):
    inline_model = None
    inline_field = None
    create_reverse_link = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        return self.validate_formset(request=request)

    def get_object(self):
        slug = self.kwargs.get(self.slug_url_field)
        try:
            obj = self.model.objects.get(**{self.slug_field: slug})
        except self.model.DoesNotExist:
            raise Http404(gettext("Not video found"))
        return obj

    def get_success_messange(self):
        return gettext(
            f"{self.model._meta.verbose_name} "
            f"{self.inline_model._meta.verbose_name_plural} saved successfully"
        )

    def get_error_menssage(self):
        return gettext(
            f"Error saving {self.model._meta.verbose_name} "
            f"{self.inline_model._meta.verbose_name_plural}"
        )

    def get_model_name_plural(self):
        return self.inline_model._meta.verbose_name_plural

    def get_extra_context(self):
        return {"object": self.object}

    def get_queryset(self):
        queryset = self.inline_model.objects.filter(**{self.inline_field: self.object})
        queryset = self.apply_filters(queryset)
        return queryset

    def get_success_url_kwargs(self):
        return {
            "collection": self.object.categorization.collection.slug,
            self.slug_url_field: getattr(self.object, self.slug_field),
        }

    def get_create_link(self):
        return reverse(
            self.create_reverse_link,
            kwargs={
                "slug": getattr(self.object, self.slug_field),
                "collection": self.object.collection_slug,
            },
        )
