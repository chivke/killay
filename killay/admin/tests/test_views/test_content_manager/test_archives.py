import pytest

from django.test import Client

from killay.archives.models import Archive
from killay.archives.tests.recipes import archive_recipe


@pytest.mark.django_db
class TestArchiveListView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        archive = archive_recipe.make()
        response = client.get("/admin/cm/archives/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].name == archive.name


@pytest.mark.django_db
class TestArchiveCreateView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/archives/~create/")
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
        response = client.post("/admin/cm/archives/~create/", data)
        assert response.status_code == 302
        archive = Archive.objects.get(name=fake_name, slug=fake_slug)
        assert archive.slug == fake_slug
        assert archive.name == fake_name


@pytest.mark.django_db
class TestArchiveUpdateView:
    def test_get(self, admin_user, client: Client):
        archive = archive_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/cm/archives/{archive.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user, client: Client):
        archive = archive_recipe.make()
        new_name = "new name"
        data = {
            "name": new_name,
            "slug": archive.slug,
            "position": archive.position,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/cm/archives/{archive.id}/", data)
        assert response.status_code == 302
        archive.refresh_from_db()
        assert archive.name == new_name
