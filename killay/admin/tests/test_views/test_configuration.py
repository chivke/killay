from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

import pytest

from killay.admin.models import SiteConfiguration
from killay.admin.tests import recipes as admin_recipes
from killay.archives.tests.recipes import archive_recipe
from killay.users.models import User
from killay.viewer.lib.constants import ViewerConstants


SOCIALMEDIA_FORMSET_DATA = {
    "social_medias-INITIAL_FORMS": "0",
    "social_medias-TOTAL_FORMS": "1",
    "social_medias-0-provider": "youtube",
    "social_medias-0-url": "http://youtube.com",
    "social_medias-0-is_visible": True,
    "social_medias-0-position": "0",
}

LOGO_FORMSET_DATA = {"logos-INITIAL_FORMS": "0", "logos-TOTAL_FORMS": "0"}

SITE_CONF_DATA = {**SOCIALMEDIA_FORMSET_DATA, **LOGO_FORMSET_DATA}


@pytest.mark.django_db
class TestConfigurationUpdateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/conf/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user: User, client: Client):
        data = {"name": "Other site name", "domain": "ex.org", "is_published": False}
        client.force_login(admin_user)
        response = client.post("/admin/conf/", data)
        assert response.status_code == 302
        conf = SiteConfiguration.objects.current()
        for field, value in data.items():
            assert getattr(conf, field) == value

    def test_update_fail(self, admin_user: User, client: Client):
        data = {"name": ""}
        client.force_login(admin_user)
        response = client.post("/admin/conf/", data)
        assert response.status_code == 200
        assert response.context_data["form"].errors


@pytest.mark.django_db
class TestViewerUpdateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/conf/viewer/")
        assert response.render()
        assert response.status_code == 200

    def test_update(self, admin_user: User, client: Client):
        archive = archive_recipe.make()
        site_conf = SiteConfiguration.objects.current()
        viewer = site_conf.viewer
        data = {
            "home": ViewerConstants.HOME_DEFAULT,
            "scope": ViewerConstants.SCOPE_ONE_ARCHIVE,
            "scope_archive": archive.id,
        }
        assert viewer.scope == ViewerConstants.SCOPE_ALL
        client.force_login(admin_user)
        response = client.post("/admin/conf/viewer/", data)
        assert response.status_code == 302
        viewer.refresh_from_db()
        assert viewer.scope == ViewerConstants.SCOPE_ONE_ARCHIVE
        assert viewer.scope_archive_id == archive.id

    def test_fail(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        data = {
            "scope": ViewerConstants.SCOPE_ONE_ARCHIVE,
        }
        response = client.post("/admin/conf/viewer/", data)
        assert response.status_code == 200
        assert response.context_data["form"].errors


@pytest.mark.django_db
class TestSiteSocialMediaListView:
    def test_get(self, admin_user: User, client: Client):
        social_media = admin_recipes.social_media_recipe.make()
        client.force_login(admin_user)
        response = client.get("/admin/conf/social-medias/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].id == social_media.id

    def test_post(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        conf = SiteConfiguration.objects.current()
        data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "1",
            "form-0-config": conf.id,
            "form-0-provider": "youtube",
            "form-0-url": "http://youtube.com",
            "form-0-is_visible": True,
            "form-0-position": "0",
        }
        response = client.post("/admin/conf/social-medias/", data)
        assert response.status_code == 302
        assert conf.social_medias.first().url == data["form-0-url"]

    def test_fail(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        conf = SiteConfiguration.objects.current()
        data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "1",
            "form-0-config": conf.id,
            "form-0-is_visible": True,
            "form-0-position": "0",
        }
        response = client.post("/admin/conf/social-medias/", data)
        assert response.status_code == 200
        assert response.context_data["formset"].errors


@pytest.mark.django_db
class TestSiteSocialMediaCreateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/conf/social-medias/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_post(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        conf = SiteConfiguration.objects.current()
        data = {
            "config": conf.id,
            "is_visible": True,
            "position": "0",
            "provider": "youtube",
            "url": "http://youtube.com",
        }
        response = client.post("/admin/conf/social-medias/~create/", data)
        assert response.status_code == 302
        assert conf.social_medias.first().url == data["url"]

    def test_fail(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        conf = SiteConfiguration.objects.current()
        data = {
            "config": conf.id,
            "is_visible": True,
            "position": "0",
        }
        response = client.post("/admin/conf/social-medias/~create/", data)
        assert response.status_code == 200
        assert response.context_data["form"].errors


@pytest.mark.django_db
class TestSiteLogoListView:
    def test_get(self, admin_user: User, client: Client):
        logo = admin_recipes.logo_recipe.make()
        client.force_login(admin_user)
        response = client.get("/admin/conf/logos/")
        assert response.render()
        assert response.status_code == 200
        assert response.context_data["object_list"][0].id == logo.id

    def test_post(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        logo = admin_recipes.logo_recipe.make()
        conf = SiteConfiguration.objects.current()
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = "img.gif"
        data = {
            "form-INITIAL_FORMS": "1",
            "form-TOTAL_FORMS": "1",
            "form-0-id": logo.id,
            "form-0-image": img,
            "form-0-configuration": conf.id,
            "form-0-name": logo.name,
            "form-0-is_visible": True,
            "form-0-position": "3",
        }
        response = client.post("/admin/conf/logos/", data)
        assert response.status_code == 302
        assert conf.logos.first().is_visible

    def test_fail(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "1",
            "form-0-is_visible": True,
            "form-0-image": "0",
        }
        response = client.post("/admin/conf/logos/", data)
        assert response.status_code == 200
        assert response.context_data["formset"].errors


@pytest.mark.django_db
class TestSiteLogoCreateView:
    def test_get(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        response = client.get("/admin/conf/logos/~create/")
        assert response.render()
        assert response.status_code == 200

    def test_post(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        conf = SiteConfiguration.objects.current()
        img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )
        img.name = "img.gif"
        logo_name = "test logo"
        data = {
            "image": img,
            "configuration": conf.id,
            "name": logo_name,
            "is_visible": True,
            "position": "3",
        }

        response = client.post("/admin/conf/logos/~create/", data)
        assert response.status_code == 302
        assert conf.logos.first().name == logo_name

    def test_fail(self, admin_user: User, client: Client):
        client.force_login(admin_user)
        conf = SiteConfiguration.objects.current()
        data = {
            "config": conf.id,
            "is_visible": True,
            "position": "0",
        }
        response = client.post("/admin/conf/logos/~create/", data)
        assert response.status_code == 200
        assert response.context_data["form"].errors
