import pytest

from django.test import RequestFactory
from django.template import Context, Template
from django.urls import resolve

from killay.videos.models import Video

pytestmark = pytest.mark.django_db


class TestShowAdminNavbar:
    def test_admin_conf(self, admin_user, rf: RequestFactory):
        request = rf.get("/admin/")
        request.user = admin_user
        request.resolver_match = resolve("/admin/")
        context = Context({"request": request})
        template_to_render = Template(
            "{% load admin_navbar %}" "{% show_admin_navbar %}"
        )
        rendered_template = template_to_render.render(context)
        assert rendered_template
        assert "item active" in rendered_template

    def test_video_detail(self, admin_user, video: Video, rf: RequestFactory):
        video.is_visible = True
        video.save()
        url = f"/videos/{video.code}/"
        request = rf.get(url)
        request.user = admin_user
        request.resolver_match = resolve(url)
        context = Context({"request": request, "object": video})
        template_to_render = Template(
            "{% load admin_navbar %}" "{% show_admin_navbar %}"
        )
        rendered_template = template_to_render.render(context)
        assert rendered_template
        assert "item active" in rendered_template
        assert video.code in rendered_template
