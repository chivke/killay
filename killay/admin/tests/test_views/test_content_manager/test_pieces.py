import pytest

from django.test import Client

from killay.archives.models import Piece
from killay.archives.tests.recipes import collection_recipe, piece_recipe


@pytest.mark.django_db
class TestPieceListView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        piece = piece_recipe.make()
        response = client.get("/admin/cm/pieces/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].title == piece.title


@pytest.mark.django_db
class TestPieceCreateView:
    def test_get(self, admin_user, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/pieces/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user, client: Client):
        fake_title = "fake_archive"
        fake_code = "fake_code"
        collection = collection_recipe.make()
        data = {
            "title": fake_title,
            "code": fake_code,
            "position": 0,
            "kind": "DOCUMENT",
            "collection": collection.id,
        }
        client.force_login(admin_user)
        response = client.post("/admin/cm/pieces/~create/", data)
        assert response.status_code == 302
        piece = Piece.objects.get(title=fake_title, code=fake_code)
        assert piece.code == fake_code
        assert piece.title == fake_title


@pytest.mark.django_db
class TestPieceUpdateView:
    def test_get(self, admin_user, client: Client):
        piece = piece_recipe.make()
        client.force_login(admin_user)
        response = client.get(f"/admin/cm/pieces/{piece.id}/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user, client: Client):
        piece = piece_recipe.make()
        new_title = "new title"
        data = {
            "title": new_title,
            "code": piece.code,
            "position": 0,
            "kind": piece.kind,
            "collection": piece.collection_id,
        }
        client.force_login(admin_user)
        response = client.post(f"/admin/cm/pieces/{piece.id}/", data)
        assert response.status_code == 302
        piece.refresh_from_db()
        assert piece.title == new_title
