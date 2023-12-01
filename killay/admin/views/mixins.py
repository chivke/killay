from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import ModelFormMixin
from django.views.generic.base import TemplateResponseMixin

from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy


from killay.admin.models import SiteConfiguration


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


class AdminView(AdminRequiredMixin, TemplateResponseMixin, View):
    template_name = "admin/base.html"
    extra_context = None
    main_title = None
    second_title = None
    description = None
    breadcrumb = None
    extra_links = None
    extra_data = {}
    extra_actions = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {}
        forms_context = self.get_forms_context(**kwargs)
        context["main_title"] = self.get_main_title()
        context["second_title"] = self.get_second_title()
        context["description"] = self.get_description()
        context["breadcrumb"] = self.get_breadcrumb()
        context["extra_links"] = self.get_extra_links()
        context["extra_data"] = self.get_extra_data()
        context["extra_actions"] = self.get_extra_actions()
        extra_context = self.get_extra_context()
        context.update(forms_context)
        context.update(extra_context)
        return {**context, **kwargs}

    def get_extra_context(self) -> dict:
        return self.extra_context or {}

    def get_forms_context(self) -> dict:
        return {}

    def get_main_title(self) -> str:
        return self.main_title

    def get_second_title(self) -> str:
        return self.second_title

    def get_description(self) -> str:
        return self.description

    def get_breadcrumb(self) -> list:
        return self.breadcrumb or []

    def get_extra_links(self) -> list:
        return self.extra_links or []

    def get_extra_data(self) -> list:
        return self.extra_data or {}

    def get_extra_actions(self) -> list:
        return self.extra_actions or []


class SingleMixin(AdminView, ModelFormMixin):
    form_class = None
    form_template = "admin/components/form.html"
    slug_field = "pk"
    pk_url_kwarg = "slug"
    name_field = "name"
    reverse_url = None
    delete_url = None
    action_name = None
    html_fields = None

    def get_forms_context(self, **kwargs) -> dict:
        self.object = self.get_object()
        context = super(ModelFormMixin, self).get_context_data(**kwargs)
        context["form_template"] = self.form_template
        context["delete_url"] = self.delete_url
        context["html_fields"] = self.html_fields
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if not self.object and self.request.GET:
            for field in form.fields:
                if field in self.request.GET:
                    form.initial[field] = self.request.GET[field]
        return form

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            message = self.get_error_message(form=form)
            messages.error(self.request, message)
            return self.form_invalid(form)

    def get_error_message(self, form):
        return form.errors.get("__all__", gettext(f"Error not {self.action_name}"))

    def get_queryset(self):
        return self.form_class.Meta.model.objects.all()

    def get_success_url(self):
        model_name = self.object._meta.verbose_name.capitalize()
        slug_value = self.get_slug_value()
        name = getattr(self.object, self.name_field)
        message = gettext(
            f'{model_name} {self.name_field}="{name}" was {self.action_name}'
        )
        messages.info(self.request, message)
        url_kwargs = {self.pk_url_kwarg: slug_value} if slug_value else {}
        return reverse(self.reverse_url, kwargs=url_kwargs)

    def get_slug_value(self):
        return getattr(self.object, self.slug_field) if self.slug_field else None

    def get_extra_data(self) -> str:
        if not self.object:
            return {}
        created_at_label = self.object.__class__.created_at.field.verbose_name
        updated_at_label = self.object.__class__.updated_at.field.verbose_name
        return {
            "ID": self.object.id,
            created_at_label: self.object.created_at,
            updated_at_label: self.object.updated_at,
        }


class CreateAdminView(SingleMixin):
    form_class = None
    action_name = "created"

    def get_object(self) -> dict:
        return

    def get_second_title(self) -> str:
        model_name = self.form_class.Meta.model._meta.verbose_name.capitalize()
        return f"Create {model_name}"


class UpdateAdminView(SingleMixin):
    form_class = None
    form_template = "admin/components/form.html"
    action_name = "updated"

    def get_second_title(self) -> str:
        model_name = self.object._meta.verbose_name.capitalize()
        name = getattr(self.object, self.name_field)
        return f'Update {model_name} "{name}"'


class DeleteAdminView(SingleMixin):
    form_class = None
    action_name = "deleted"
    form_template = "admin/components/delete.html"
    reverse_url = None

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_second_title(self) -> str:
        model_name = self.object._meta.verbose_name.capitalize()
        name = getattr(self.object, self.name_field)
        return f'Delete {model_name} "{name}"'

    def get_slug_value(self):
        return


class FormSetMixin:
    manager_name = "objects"
    paginator_class = Paginator
    formset_class = None
    search_field = "name"
    reverse_url = None
    create_url = None
    update_url = None
    delete_url = None
    formset_template = "admin/components/formset.html"
    paginate_by = 50
    compact_fields = []
    filters = None
    extra_context = {}
    filter_applied = {}
    page_kwarg = "page"
    image_fields = []
    row_extra_template = None

    @property
    def model(self):
        formset_class = self.get_formset_class()
        return formset_class.model

    def get_forms_context(self, **kwargs) -> dict:
        context = {}
        if self.filters:
            context["filter_options"] = self.get_filter_options()
        object_list = self.get_queryset()
        context["total_of_objects"] = self.total_of_objects
        context["formset_template"] = self.formset_template
        context["query_search"] = self.query_search
        context["filter_applied"] = self.filter_applied
        context["compact_fields"] = self.compact_fields
        context["image_fields"] = self.image_fields
        context.update(self.pagination_context)
        context["create_link"] = self.get_create_link()
        context["delete_url"] = self.delete_url
        context["update_url"] = self.update_url
        context["row_extra_template"] = self.row_extra_template
        if "formset" not in kwargs:
            kwargs["formset"] = self.get_formset(queryset=object_list)
        return {**context, **kwargs}

    def get_formset(self, *args, **kwargs):
        formset_class = self.get_formset_class()
        return formset_class(*args, **kwargs)

    def get_formset_class(self):
        return self.formset_class

    def get_extra_data(self) -> dict:
        return {"Total": self.total_of_objects}

    def get_filter_options(self):
        return {}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.validate_formset(request=request)

    def get_queryset(self):
        manager = getattr(self.model, self.manager_name)
        queryset = manager.all()
        queryset = self.apply_filters(queryset)
        return queryset

    def apply_filters(self, queryset):
        queryset = self.set_search_filter_if_exists(queryset)
        queryset = self.set_custom_filter_if_exists(queryset)
        self.total_of_objects = queryset.count()
        page_size = self.paginate_by
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

    def get_create_link(self):
        return reverse(self.create_url)

    def validate_formset(self, request, **kwargs):
        formset = self.get_formset(
            data=request.POST, files=request.FILES, queryset=self.object_list, **kwargs
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

    def get_success_url_kwargs(self):
        return {}

    def get_success_messange(self):
        return gettext(f"{self.model._meta.verbose_name_plural} saved successfully")

    def get_error_menssage(self):
        return gettext(f"Error saving {self.model._meta.verbose_name_plural}")

    def paginate_queryset(self, queryset, page_size):
        paginator = self.paginator_class(
            queryset,
            page_size,
            orphans=0,
            allow_empty_first_page=True,
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                raise Http404(
                    gettext_lazy(
                        "Page is not “last”, nor can it be converted to an int."
                    )
                )
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(
                gettext_lazy("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )


class FormSetAdminView(FormSetMixin, AdminView):
    pass


class InlineFormSetAdminView(FormSetAdminView):
    parent_manager_name = "objects"
    parent_model = None
    related_field = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        return self.validate_formset(request=request)

    def get_object(self):
        parent_manager = getattr(self.parent_model, self.parent_manager_name)
        object_id = self.kwargs.get("slug")
        try:
            obj = parent_manager.get(id=object_id)
        except self.parent_model.DoesNotExist:
            message = gettext(f"{self.parent_model.Meta.verbose_name} not exists")
            raise Http404(message)
        return obj

    def get_forms_context(self, **kwargs) -> dict:
        self.object = self.get_object()
        kwargs["object"] = self.object
        return super().get_forms_context(**kwargs)

    def get_queryset(self):
        manager = getattr(self.model, self.manager_name)
        inline_filter = {self.related_field: self.object.id}
        queryset = manager.filter(**inline_filter)
        queryset = self.apply_filters(queryset)
        return queryset

    def get_success_url_kwargs(self):
        return {"slug": self.object.id}
