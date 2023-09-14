import pytest

from django.test import Client

from killay.archives.models import Keyword
from killay.archives.tests.recipes import keyword_recipe


@pytest.mark.django_db
class TestKeywordListView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        keyword = keyword_recipe.make()
        response = client.get("/admin/cm/keywords/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].name == keyword.name


@pytest.mark.django_db
class TestKeywordCreateView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/keywords/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user, client: Client):
        fake_name = "fake_archive"
        fake_slug = "fake_slug"
        data = {
            "name": fake_name,
            "slug": fake_slug,
            "position": 0,
        }
        client.force_login(admin_user)
        response = client.post("/admin/cm/keywords/~create/", data)
        assert response.status_code == 302
        keyword = Keyword.objects.get(name=fake_name, slug=fake_slug)
        assert keyword.slug == fake_slug
        assert keyword.name == fake_name


@pytest.mark.django_db
class TestKeywordUpdateView:
    def test_get(self, admin_user, client: Client):
        keyword = keyword_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/cm/keywords/{keyword.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user, client: Client):
        keyword = keyword_recipe.make()
        new_name = "new name"
        data = {
            "name": new_name,
            "slug": keyword.slug,
            "position": keyword.position,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/cm/keywords/{keyword.id}/", data)
        assert response.status_code == 302
        keyword.refresh_from_db()
        assert keyword.name == new_name
