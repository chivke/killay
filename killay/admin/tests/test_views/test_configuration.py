import pytest

from django.test import RequestFactory, Client
from django.urls import resolve

from killay.admin.models import SiteConfiguration
from killay.admin.views.configuration import admin_site_configuration_view

from killay.users.models import User


pytestmark = pytest.mark.django_db


SOCIALMEDIA_FORMSET_DATA = {
    "social_medias-INITIAL_FORMS": "0",
    "social_medias-TOTAL_FORMS": "1",
    "social_medias-0-provider": "youtube",
    "social_medias-0-url": "http://youtube.com",
    "social_medias-0-is_visible": True,
    "social_medias-0-position": "0",
}

LOGO_FORMSET_DATA = {"logos-INITIAL_FORMS": "0", "logos-TOTAL_FORMS": "0"}

SITE_CONF_DATA = {**SOCIALMEDIA_FORMSET_DATA, **LOGO_FORMSET_DATA}


class TestConfigurationUpdateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/conf/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user: User, client: Client):
        data = {"name": "Other site name", "domain": "ex.org", "is_published": False}
        client.force_login(admin_user)
        response = client.post("/admin/conf/", {**data})
        assert response.status_code == 302
        conf = SiteConfiguration.objects.current()
        for field, value in data.items():
            assert getattr(conf, field) == value

    def test_update_fail(self, admin_user: User, client: Client):
        data = {"name": ""}
        client.force_login(admin_user)
        response = client.post("/admin/conf/", data)
        assert response.status_code == 200
        assert response.context_data["form"].errors
