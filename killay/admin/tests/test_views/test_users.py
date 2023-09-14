import pytest

from django.test import Client

from killay.users.models import User


@pytest.mark.django_db
class TestUserListView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/users/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].username == admin_user.username


@pytest.mark.django_db
class TestUserCreateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/users/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user: User, client: Client):
        data = {
            "username": "fake_user",
            "email": "fake@localhost",
            "password1": "1",
            "password2": "1",
        }
        client.force_login(admin_user)
        response = client.post("/admin/users/~create/", data)
        assert response.status_code == 302
        user = User.objects.get(username=data["username"])
        assert user.email == data["email"]


@pytest.mark.django_db
class TestUserUpdateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get(f"/admin/users/{admin_user.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user: User, client: Client):
        new_email = "fake@localhost"
        data = {
            "username": admin_user.username,
            "email": new_email,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/users/{admin_user.id}/", data)
        assert response.status_code == 302
        admin_user.refresh_from_db()
        assert admin_user.email == new_email
