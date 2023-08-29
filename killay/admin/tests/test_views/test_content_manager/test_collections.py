import pytest

from django.test import Client

from killay.archives.models import Collection
from killay.archives.tests.recipes import archive_recipe, collection_recipe


@pytest.mark.django_db
class TestCollectionListView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        collection = collection_recipe.make()
        response = client.get("/admin/cm/collections/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].name == collection.name


@pytest.mark.django_db
class TestCollectionCreateView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/collections/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user, client: Client):
        fake_name = "fake_archive"
        fake_slug = "fake_slug"
        archive = archive_recipe.make()
        data = {
            "name": fake_name,
            "slug": fake_slug,
            "position": 0,
            "archive": archive.id,
        }
        client.force_login(admin_user)
        response = client.post("/admin/cm/collections/~create/", data)
        assert response.status_code == 302
        collection = Collection.objects.get(name=fake_name, slug=fake_slug)
        assert collection.slug == fake_slug
        assert collection.name == fake_name


@pytest.mark.django_db
class TestCollectionUpdateView:
    def test_get(self, admin_user, client: Client):
        collection = collection_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/cm/collections/{collection.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user, client: Client):
        collection = collection_recipe.make()
        new_name = "new name"
        data = {
            "name": new_name,
            "slug": collection.slug,
            "position": collection.position,
            "archive": collection.archive_id,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/cm/collections/{collection.id}/", data)
        assert response.status_code == 302
        collection.refresh_from_db()
        assert collection.name == new_name
