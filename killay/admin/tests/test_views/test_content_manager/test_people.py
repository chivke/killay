import pytest

from django.test import Client

from killay.archives.models import Person
from killay.archives.tests.recipes import person_recipe


@pytest.mark.django_db
class TestPersonListView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        person = person_recipe.make()
        response = client.get("/admin/cm/people/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].name == person.name


@pytest.mark.django_db
class TestPersonCreateView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/people/~create/")
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
        response = client.post("/admin/cm/people/~create/", data)
        assert response.status_code == 302
        category = Person.objects.get(name=fake_name, slug=fake_slug)
        assert category.slug == fake_slug
        assert category.name == fake_name


@pytest.mark.django_db
class TestPersonUpdateView:
    def test_get(self, admin_user, client: Client):
        person = person_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/cm/people/{person.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user, client: Client):
        person = person_recipe.make()
        new_name = "new name"
        data = {
            "name": new_name,
            "slug": person.slug,
            "position": person.position,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/cm/people/{person.id}/", data)
        assert response.status_code == 302
        person.refresh_from_db()
        assert person.name == new_name
