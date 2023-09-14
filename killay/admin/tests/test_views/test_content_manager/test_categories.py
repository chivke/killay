import pytest

from django.test import Client

from killay.archives.models import Category
from killay.archives.tests.recipes import category_recipe, collection_recipe


@pytest.mark.django_db
class TestCategoryListView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        category = category_recipe.make()
        response = client.get("/admin/cm/categories/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].name == category.name


@pytest.mark.django_db
class TestCategoriesCreateView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/categories/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user, client: Client):
        fake_name = "fake_archive"
        fake_slug = "fake_slug"
        collection = collection_recipe.make()
        data = {
            "name": fake_name,
            "slug": fake_slug,
            "position": 0,
            "collection": collection.id,
        }
        client.force_login(admin_user)
        response = client.post("/admin/cm/categories/~create/", data)
        assert response.status_code == 302
        category = Category.objects.get(name=fake_name, slug=fake_slug)
        assert category.slug == fake_slug
        assert category.name == fake_name


@pytest.mark.django_db
class TestCategoryUpdateView:
    def test_get(self, admin_user, client: Client):
        category = category_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/cm/categories/{category.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user, client: Client):
        category = category_recipe.make()
        new_name = "new name"
        data = {
            "name": new_name,
            "slug": category.slug,
            "position": category.position,
            "collection": category.collection_id,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/cm/categories/{category.id}/", data)
        assert response.status_code == 302
        category.refresh_from_db()
        assert category.name == new_name
