import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from cmpirque.admin.mixins import AdminRequiredMixin, PublishRequiredMixin
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
