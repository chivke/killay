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


def _get_extra_links(current_name: Optional[str] = None) -> list:
    extra_links = []
    for name, pattern in SiteConfigurationConstants.PATTERN_BY_NAME.items():
        extra_link = {"name": name}
        if name != current_name:
            extra_link["link"] = reverse(pattern)
        extra_links.append(extra_link)
    return extra_links


class ConfigurationUpdateView(UpdateAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    description = SiteConfigurationConstants.DESCRIPTION_GENERAL
    form_class = SiteConfigurationForm
    reverse_url = "admin:site_configuration"

    def get_object(self):
        return self.request.site_configuration

    def get_extra_data(self) -> str:
        return {}

    def get_second_title(self) -> str:
        return SiteConfigurationConstants.NAME_GENERAL

    def get_extra_links(self):
        return _get_extra_links(current_name=SiteConfigurationConstants.NAME_GENERAL)

    def get_slug_value(self):
        return


admin_site_configuration_view = ConfigurationUpdateView.as_view()


class ViewerUpdateView(UpdateAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    description = SiteConfigurationConstants.DESCRIPTION_VIEWER
    form_class = ViewerForm
    reverse_url = SiteConfigurationConstants.PATTERN_VIEWER
    name_field = "id"

    def get_object(self):
        return self.request.site_configuration.viewer

    def get_extra_data(self) -> str:
        return {}

    def get_second_title(self) -> str:
        return SiteConfigurationConstants.NAME_VIEWER

    def get_extra_links(self):
        return _get_extra_links(current_name=SiteConfigurationConstants.NAME_VIEWER)

    def get_slug_value(self):
        return


admin_site_viewer_view = ViewerUpdateView.as_view()


class SiteSocialMediaListView(FormSetAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    second_title = SiteConfigurationConstants.NAME_SOCIAL_MEDIA
    description = SiteConfigurationConstants.DESCRIPTION_SOCIAL_MEDIA
    formset_class = SocialMediaFormSet
    reverse_url = "admin:site_social_media_list"
    create_url = "admin:site_social_media_create"
    manager_name = "objects_in_site"

    def get_extra_links(self):
        return _get_extra_links(
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

    def get_extra_links(self):
        return _get_extra_links()


admin_site_social_media_create_view = SiteSocialMediaCreateView.as_view()


class SiteLogoListView(FormSetAdminView):
    main_title = SiteConfigurationConstants.MAIN_TITLE
    second_title = SiteConfigurationConstants.NAME_LOGO
    description = SiteConfigurationConstants.DESCRIPTION_LOGO
    formset_class = LogoFormSet
    reverse_url = "admin:site_logo_list"
    create_url = "admin:site_logo_create"
    manager_name = "objects_in_site"
    image_fields = ["image"]

    def get_extra_links(self):
        return _get_extra_links(current_name=SiteConfigurationConstants.NAME_LOGO)


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

    def get_extra_links(self):
        return _get_extra_links()


admin_site_logo_create_view = SiteLogoCreateView.as_view()
