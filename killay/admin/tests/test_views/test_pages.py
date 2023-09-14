import pytest

from django.test import Client

from killay.pages.models import Page
from killay.pages.tests.recipes import page_recipe
from killay.users.models import User


@pytest.mark.django_db
class TestUserListView:
    def test_get(self, admin_user: User, client: Client):
        page = page_recipe.make()
        client.force_login(admin_user)
        response = client.get("/admin/pages/")
        assert response.render()
        assert response.status_code == 200
        assert page.title in [
            page.title for page in response.context_data["object_list"]
        ]


@pytest.mark.django_db
class TestPageCreateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/pages/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user: User, client: Client):
        data = {
            "title": "fake page",
            "slug": "fake-page",
            "kind": "PAGE",
            "position": 9,
        }
        client.force_login(admin_user)
        response = client.post("/admin/pages/~create/", data)
        assert response.status_code == 302
        page = Page.objects.get(slug=data["slug"])
        assert page.title == data["title"]


@pytest.mark.django_db
class TestUPageUpdateView:
    def test_get(self, admin_user: User, client: Client):
        page = page_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/pages/{page.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user: User, client: Client):
        page = page_recipe.make()
        new_title = "fake title"
        data = {
            "slug": page.slug,
            "title": new_title,
            "kind": page.kind,
            "position": page.position,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/pages/{page.id}/", data)
        assert response.status_code == 302
        page.refresh_from_db()
        assert page.title == new_title
