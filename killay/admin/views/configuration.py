from typing import Optional

from django.urls import reverse

from killay.admin.lib.constants import SiteConfigurationConstants
from killay.admin.forms import (
    LogoForm,
    LogoFormSet,
    SiteConfigurationForm,
    SocialMediaForm,
    SocialMediaFormSet,
    ViewerForm,
)
from killay.admin.views.mixins import CreateAdminView, FormSetAdminView, UpdateAdminView


def _get_extra_actions(current_name: Optional[str] = None) -> list:
    extra_actions = []
    for name, pattern in SiteConfigurationConstants.PATTERN_BY_NAME.items():
        extra_action = {"name": name}
        if name != current_name:
            extra_action["link"] = reverse(pattern)
        extra_actions.append(extra_action)
    return extra_actions


class ConfigurationUpdateView(UpdateAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    form_class = SiteConfigurationForm
    reverse_url = "admin:site_configuration"

    def get_object(self):
        return self.request.site_configuration

    def get_extra_data(self) -> str:
        return {}

    def get_second_title(self) -> str:
        return

    def get_extra_actions(self):
        return _get_extra_actions(current_name=SiteConfigurationConstants.NAME_GENERAL)

    def get_slug_value(self):
        return


admin_site_configuration_view = ConfigurationUpdateView.as_view()


class ViewerUpdateView(UpdateAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    form_class = ViewerForm
    reverse_url = "admin:site_configuration"

    def get_object(self):
        return self.request.site_configuration.viewer

    def get_extra_data(self) -> str:
        return {}

    def get_second_title(self) -> str:
        return

    def get_extra_actions(self):
        return _get_extra_actions(current_name=SiteConfigurationConstants.NAME_VIEWER)

    def get_slug_value(self):
        return


admin_site_viewer_view = ViewerUpdateView.as_view()


class SiteSocialMediaListView(FormSetAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    formset_class = SocialMediaFormSet
    reverse_url = "admin:site_social_media_list"
    create_url = "admin:site_social_media_create"
    manager_name = "objects_in_site"

    def get_extra_actions(self):
        return _get_extra_actions(
            current_name=SiteConfigurationConstants.NAME_SOCIAL_MEDIA
        )


admin_site_social_media_list_view = SiteSocialMediaListView.as_view()


class SiteSocialMediaCreateView(CreateAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    form_class = SocialMediaForm
    reverse_url = "admin:site_social_media_list"
    name_field = "provider"

    def get_form(self, *args, **kwargs):
        config = self.request.site_configuration
        form = super().get_form(*args, **kwargs)
        form.initial["config"] = config.id
        return form

    def get_slug_value(self):
        return

    def get_extra_actions(self):
        return _get_extra_actions()


admin_site_social_media_create_view = SiteSocialMediaCreateView.as_view()


class SiteLogoListView(FormSetAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    formset_class = LogoFormSet
    reverse_url = "admin:site_logo_list"
    create_url = "admin:site_logo_create"
    manager_name = "objects_in_site"
    image_fields = ["image"]

    def get_extra_actions(self):
        return _get_extra_actions(current_name=SiteConfigurationConstants.NAME_LOGO)


admin_site_logo_list_view = SiteLogoListView.as_view()


class SiteLogoCreateView(CreateAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    form_class = LogoForm
    reverse_url = "admin:site_social_media_create"

    def get_form(self, *args, **kwargs):
        config = self.request.site_configuration
        form = super().get_form(*args, **kwargs)
        form.initial["configuration"] = config.id
        return form

    def get_slug_value(self):
        return

    def get_extra_actions(self):
        return _get_extra_actions()


admin_site_logo_create_view = SiteLogoCreateView.as_view()
