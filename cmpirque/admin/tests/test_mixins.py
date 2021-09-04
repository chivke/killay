import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from cmpirque.admin.mixins import (
    AdminRequiredMixin,
    PublishRequiredMixin,
    AdminListMixin,
    AdminUpdateMixin,
)
from cmpirque.admin.models import SiteConfiguration


pytestmark = pytest.mark.django_db


class TestAdminRequiredMixin:
    def test_is_not_superuser(self, rf: RequestFactory):
        request = rf.get("/")
        request.user = AnonymousUser()
        mixin = AdminRequiredMixin()
        mixin.request = request
        response = mixin.dispatch(request)
        assert response.status_code == 302
        assert "login" in response.url

    def test_is_superuser(self, admin_user, rf: RequestFactory):
        request = rf.get("/")
        request.user = admin_user
        mixin = AdminRequiredMixin()
        mixin.request = request
        attribute_error = None
        with pytest.raises(AttributeError) as error:
            attribute_error = error
            mixin.dispatch(request)
        assert "dispatch" in attribute_error.value.args[0]


class TestPublishRequiredMixin:
    def test_is_not_pusblished(self, rf: RequestFactory):
        conf = SiteConfiguration.objects.current()
        conf.is_published = False
        conf.save()
        request = rf.get("/")
        request.user = AnonymousUser()
        mixin = PublishRequiredMixin()
        mixin.request = request
        response = mixin.dispatch(request)
        assert response.status_code == 302
        assert "login" in response.url


class TestAdminListMixin:
    def test_get_object_list_values(self, user):
        mixin = AdminListMixin()
        mixin.slug_key = "username"
        mixin.object_action_links = {
            "update_object": {"name": "x", "link": "admin:users_update"}
        }
        mixin.object_list = user.__class__.objects.all()
        mixin.list_fields = ["username"]
        result = mixin.get_object_list_values()
        assert len(result) == 1
        assert "username" in result[0]
        assert "actions" in result[0]
        assert "update_object" in result[0]["actions"]

    def test_get_context_data(self, user):
        mixin = AdminListMixin()
        mixin.model = user.__class__
        mixin.slug_key = "username"
        mixin.object_action_links = {
            "update_object": {"name": "x", "link": "admin:users_update"}
        }
        mixin.object_list = user.__class__.objects.all()
        mixin.list_fields = ["username"]
        context = mixin.get_context_data()
        assert "list_title" in context
        assert "list_fields" in context
        assert "model_fields" in context
        assert "object_list_values" in context


class TestAdminUpdateMixin:
    def test_get_success_url(self, user, rf_msg):
        mixin = AdminUpdateMixin()
        mixin.request = rf_msg("get", "/")
        mixin.model = user.__class__
        mixin.object = user
        mixin.fields = ["username"]
        mixin.slug_field = "username"
        mixin.reverse_success_url = "admin:users_update"
        url = mixin.get_success_url()
        assert url == reverse("admin:users_update", kwargs={"slug": user.username})

    def test_get_context_data(self, user, rf_msg):
        mixin = AdminUpdateMixin()
        mixin.request = rf_msg("get", "/")
        mixin.model = user.__class__
        mixin.object = user
        mixin.fields = ["username"]
        mixin.slug_key = "username"
        mixin.object_action_links = {
            "update_object": {"name": "x", "link": "admin:users_update"}
        }
        mixin.object_list = user.__class__.objects.all()
        mixin.list_fields = ["username"]
        mixin.read_only_fields = ["date_joined"]
        context = mixin.get_context_data()
        assert "read_only_fields" in context
        assert "form_title" in context
