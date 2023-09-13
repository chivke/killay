from django.http import Http404, HttpResponse
from django.urls import reverse

from killay.admin.engine.bulk_actions.forms import BulkActionForm
from killay.admin.engine.bulk_actions.templates import BulkActionTemplateProvider
from killay.admin.lib.constants import BulkActionConstants, ContentManagerConstants
from killay.admin.views.content_manager import get_content_manager_extra_links
from killay.admin.views.mixins import AdminView, CreateAdminView


BULK_ACTION_SLUG = ContentManagerConstants.SLUG_BULK_ACTION
BULK_ACTION_EXTRA_LINKS = get_content_manager_extra_links(view_slug=BULK_ACTION_SLUG)
BULK_ACTION_PATTERN = "admin:bulk_action"


class BulkActionListView(AdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[BULK_ACTION_SLUG]
    extra_links = BULK_ACTION_EXTRA_LINKS
    description = ContentManagerConstants.DESCRIPTION_BULK_ACTION

    def get_extra_actions(self) -> list:
        return [
            {
                "link": reverse(BULK_ACTION_PATTERN, kwargs={"action": action_type}),
                "name": BulkActionConstants.TYPE_NAMES[action_type],
                "desc": BulkActionConstants.TYPE_DESCRIPTIONS[action_type],
            }
            for action_type in BulkActionConstants.TYPES
        ]


bulk_action_list_view = BulkActionListView.as_view()


class BulkActionMixin:
    def dispatch(self, request, action: str, *args, **kwargs):
        if action not in BulkActionConstants.TYPES:
            raise Http404
        self.action_type = action
        return super().dispatch(request, *args, **kwargs)


class BulkActionView(BulkActionMixin, CreateAdminView):
    main_title = ContentManagerConstants.MAIN_TITLE
    second_title = ContentManagerConstants.VIEWS_SECOND_TITLE[BULK_ACTION_SLUG]
    extra_links = BULK_ACTION_EXTRA_LINKS
    form_template = "admin/components/bulk_action.html"
    form_class = BulkActionForm

    def get_breadcrumb(self) -> list:
        return [
            ContentManagerConstants.DICT_LINK[BULK_ACTION_SLUG]["list"],
            {"name": BulkActionConstants.TYPE_NAMES[self.action_type]},
        ]

    def get_second_title(self) -> str:
        return BulkActionConstants.TYPE_NAMES[self.action_type]

    def get_description(self) -> str:
        return BulkActionConstants.TYPE_DESCRIPTIONS[self.action_type]

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs.pop("instance")
        kwargs["action_type"] = self.action_type
        return kwargs

    def get_forms_context(self, **kwargs) -> dict:
        context = super().get_forms_context(**kwargs)
        context["file_headers"] = context["form"].get_file_headers_context()
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["result"] = {
            "is_valid": False,
            "data_errors": form.errors.get("__all__"),
            "file_errors": form.errors.get("xls_file"),
            "title": BulkActionConstants.RESULT_ERROR_TITLE,
            "data_errors_label": BulkActionConstants.RESULT_DATA_ERRORS_LABEL,
            "file_errors_label": BulkActionConstants.RESULT_FILE_ERRORS_LABEL,
        }
        return self.render_to_response(context)

    def get_error_message(self, form):
        return BulkActionConstants.RESULT_ERROR_TITLE

    def form_valid(self, form):
        success_data = form.save()
        context = self.get_context_data(form=form)
        context["result"] = {
            "is_valid": True,
            "data_success": success_data,
            "title": BulkActionConstants.RESULT_SUCCESS_TITLE,
        }
        return self.render_to_response(context)


bulk_action_view = BulkActionView.as_view()


class BulkActionTemplateView(BulkActionMixin, AdminView):
    def get(self, request, *args, **kwargs):
        provider = BulkActionTemplateProvider(action_type=self.action_type)
        workbook = provider.get()
        filename = provider.get_filename()
        response = HttpResponse(content_type=BulkActionConstants.FILE_CONTENT_TYPE)
        workbook.save(response)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Content-Length"] = len(response.content)
        return response


bulk_action_template_view = BulkActionTemplateView.as_view()
