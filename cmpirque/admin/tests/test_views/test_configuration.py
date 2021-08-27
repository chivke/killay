import pytest

from django.test import RequestFactory
from django.urls import resolve

from cmpirque.admin.models import AdminConfiguration
from cmpirque.admin.views.configuration import admin_configuration_view

from cmpirque.users.models import User


pytestmark = pytest.mark.django_db


SOCIALMEDIA_FORMSET_DATA = {
    "social_medias-INITIAL_FORMS": "0",
    "social_medias-TOTAL_FORMS": "1",
    "social_medias-0-provider": "youtube",
    "social_medias-0-url": "http://youtube.com",
    "social_medias-0-css_class": "youtube-class",
    "social_medias-0-is_visible": True,
}


class TestAdminConfigurationView:
    def test_get(self, admin_user: User, rf: RequestFactory):
        request = rf.get("/admin/")
        request.resolver_match = resolve("/admin/")
        request.user = admin_user
        response = admin_configuration_view(request)
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user: User, rf: RequestFactory):
        data = {"site_name": "Other site name", "is_published": False}
        request = rf.post("/admin/", {**data, **SOCIALMEDIA_FORMSET_DATA})
        request.user = admin_user
        response = admin_configuration_view(request)
        assert response.status_code == 302
        conf = AdminConfiguration.objects.current()
        for field, value in data.items():
            assert getattr(conf, field) == value
        social_media = conf.social_medias.first()
        assert social_media.provider == "youtube"
        assert social_media.url == "http://youtube.com"
        assert social_media.css_class == "youtube-class"
        assert social_media.is_visible is True

    def test_update_fail(self, admin_user: User, rf: RequestFactory):
        data = {**SOCIALMEDIA_FORMSET_DATA}
        data.pop("social_medias-0-provider")
        request = rf.post("/admin/", SOCIALMEDIA_FORMSET_DATA)
        request.user = admin_user
        response = admin_configuration_view(request)
        assert response.status_code == 200
        assert response.context_data["form"].errors
        assert response.context_data["formset"].errors
