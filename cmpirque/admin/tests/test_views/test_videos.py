import pytest

from django.test import RequestFactory
from django.urls import resolve

from cmpirque.videos.models import Video, VideoCategory, VideoPerson, VideoKeyword
from cmpirque.admin.views.videos import (
    video_categories_view,
    video_categorization,
    video_create_view,
    video_delete_view,
    video_keywords_view,
    video_update_view,
    video_people_view,
    video_sequences_list,
)
from cmpirque.users.models import User


pytestmark = pytest.mark.django_db


PROVIDERS_FORMSET_DATA = {
    "providers-INITIAL_FORMS": "0",
    "providers-TOTAL_FORMS": "1",
    "providers-0-active": "",
    "providers-0-ply_embed_id": "",
    "providers-0-plyr_provider": "",
}


class TestVideoCreateView:
    def test_get(self, admin_user: User, rf: RequestFactory):
        request = rf.get("/admin/videos/~create/")
        request.resolver_match = resolve("/admin/videos/~create/")
        request.user = admin_user
        response = video_create_view(request)
        assert response.render()
        assert response.status_code == 200

    def test_create(self, admin_user: User, rf_msg: RequestFactory):
        data = {"code": "fake", "title": "fake"}
        data_formset = {**PROVIDERS_FORMSET_DATA}
        data_formset["providers-0-plyr_provider"] = "vimeo"
        data_formset["providers-0-ply_embed_id"] = "vimeo"
        data.update(data_formset)
        request = rf_msg("post", "/admin/videos/~create/", data)
        request.user = admin_user
        response = video_create_view(request)
        assert response.status_code == 302
        video = Video.objects.get(code="fake")
        assert video.code == data["code"]
        assert video.meta.title == data["title"]
        assert video.providers.first().ply_embed_id == "vimeo"

    def test_fail_create(self, admin_user: User, rf_msg: RequestFactory):
        data = {"code": "fake"}
        data_formset = {**PROVIDERS_FORMSET_DATA}
        data_formset["providers-0-plyr_provider"] = "X"
        data.update(data_formset)
        request = rf_msg("post", "/admin/videos/~create/", data)
        request.user = admin_user
        response = video_create_view(request)
        assert response.status_code == 200
        assert "title" in response.context_data["meta_form"].errors
        assert "plyr_provider" in response.context_data["providers_formset"].errors[0]


class TestVideoUpdateView:
    def test_get(self, admin_user: User, video: Video, rf: RequestFactory):
        url = f"/admin/videos/{video.code}/~update/"
        request = rf.get(url)
        request.user = admin_user
        request.resolver_match = resolve(url)
        response = video_update_view(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_update(self, admin_user: User, video: Video, rf_msg: RequestFactory):
        data = {"code": "fake", "title": "fake"}
        data.update(PROVIDERS_FORMSET_DATA)
        request = rf_msg("post", f"/admin/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_update_view(request, slug=video.code)
        video.refresh_from_db()
        assert response.status_code == 302
        assert video.code == data["code"]
        assert video.meta.title == data["title"]

    def test_fail_update(self, admin_user: User, video: Video, rf_msg: RequestFactory):
        data = {"code": "fake"}
        data.update(PROVIDERS_FORMSET_DATA)
        request = rf_msg("post", f"/admin/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_update_view(request, slug=video.code)
        assert response.status_code == 200
        assert "title" in response.context_data["meta_form"].errors


class TestVideoDeleteView:
    def test_get(self, admin_user: User, video: Video, rf: RequestFactory):
        url = f"/admin/videos/{video.code}/~delete/"
        request = rf.get(url)
        request.user = admin_user
        request.resolver_match = resolve(url)
        response = video_delete_view(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.code in str(response.content)

    def test_delete(self, admin_user: User, video: Video, rf_msg: RequestFactory):
        data = {"code": "fake", "title": "fake"}
        request = rf_msg("post", f"/admin/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_delete_view(request, slug=video.code)
        with pytest.raises(Video.DoesNotExist):
            video.refresh_from_db()
        assert response.status_code == 302


SEQUENCES_FORMSET_DATA = {
    "sequences-INITIAL_FORMS": "0",
    "sequences-TOTAL_FORMS": "1",
    "sequences-0-title": "seq1",
    "sequences-0-ini": "00:01:00",
    "sequences-0-end": "00:02:00",
}


class TestVideoSequencesListView:
    def test_get(self, admin_user: User, video: Video, rf: RequestFactory):
        url = f"/admin/videos/{video.code}/~sequences/"
        request = rf.get(url)
        request.user = admin_user
        request.resolver_match = resolve(url)
        response = video_sequences_list(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_update(self, admin_user: User, video: Video, rf_msg: RequestFactory):
        request = rf_msg(
            "post", f"/admin/videos/{video.code}/~update/", SEQUENCES_FORMSET_DATA
        )
        request.user = admin_user
        response = video_sequences_list(request, slug=video.code)
        assert response.status_code == 302
        sequence = video.sequences.first()
        assert sequence.title == SEQUENCES_FORMSET_DATA["sequences-0-title"]
        assert str(sequence.ini) == SEQUENCES_FORMSET_DATA["sequences-0-ini"]
        assert str(sequence.end) == SEQUENCES_FORMSET_DATA["sequences-0-end"]

    def test_fail_update(self, admin_user: User, video: Video, rf_msg: RequestFactory):
        data = SEQUENCES_FORMSET_DATA
        data["sequences-0-end"] = "00:00:01"
        request = rf_msg("post", f"/admin/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_sequences_list(request, slug=video.code)
        assert response.status_code == 200
        assert "__all__" in response.context_data["formset"].errors[0]


class TestVideoCategorizationUpdateView:
    def test_get(self, admin_user: User, video: Video, rf: RequestFactory):
        url = f"/admin/videos/{video.code}/~categorization/"
        request = rf.get(url)
        request.user = admin_user
        request.resolver_match = resolve(url)
        response = video_categorization(request, slug=video.code)
        assert response.status_code == 200
        assert response.render()
        assert video.meta.title in str(response.content)

    def test_update(
        self,
        admin_user: User,
        rf_msg: RequestFactory,
        video: Video,
        video_category: VideoCategory,
        video_person: VideoPerson,
        video_keyword: VideoKeyword,
    ):
        data = {
            "categories": [video_category.id],
            "people": [video_person.id],
            "keywords": [video_keyword.id],
        }
        request = rf_msg("post", f"/admin/videos/{video.code}/~categorization/", data)
        request.user = admin_user
        response = video_categorization(request, slug=video.code)
        assert response.status_code == 302
        video.refresh_from_db()
        assert video.categorization.categories.first() == video_category
        assert video.categorization.people.first() == video_person
        assert video.categorization.keywords.first() == video_keyword

    def test_fail_update(self, admin_user: User, video: Video, rf_msg: RequestFactory):
        data = {"categories": [0]}
        request = rf_msg("post", f"/admin/videos/{video.code}/~update/", data)
        request.user = admin_user
        response = video_categorization(request, slug=video.code)
        assert response.status_code == 200
        assert "categories" in response.context_data["form"].errors


CATEGORY_FORMSET_DATA = {
    "form-TOTAL_FORMS": "2",
    "form-INITIAL_FORMS": "1",
    "form-0-name": "name1",
    "form-0-slug": "slug1",
    "form-0-description": "description1",
    "form-0-position": "0",
    "form-1-name": "name2",
    "form-1-slug": "slug2",
    "form-1-description": "description2",
    "form-1-position": "1",
}


class TestVideoCategoryListView:
    def test_get(
        self, admin_user: User, video_category: VideoCategory, rf: RequestFactory
    ):
        request = rf.get("/admin/videos/~categories/")
        request.user = admin_user
        request.resolver_match = resolve("/admin/videos/~categories/")
        response = video_categories_view(request)
        assert response.status_code == 200
        assert response.render()
        assert video_category.name in str(response.content)

    def test_update(
        self, admin_user: User, video_category: VideoCategory, rf_msg: RequestFactory
    ):
        data = {
            **CATEGORY_FORMSET_DATA,
            "form-0-id": video_category.id,
            "form-0-name": video_category.name,
            "form-0-slug": video_category.slug,
            "form-0-description": "X",
        }
        request = rf_msg("post", "/admin/videos/~categories/", data)
        request.user = admin_user
        response = video_categories_view(request)
        video_category.refresh_from_db()
        assert response.status_code == 302
        assert VideoCategory.objects.filter(slug="slug2").exists()
        assert video_category.description == "X"

    def test_fail_update(
        self, admin_user: User, video_category: VideoCategory, rf_msg: RequestFactory
    ):
        data = {
            **CATEGORY_FORMSET_DATA,
            "form-0-id": video_category.id,
            "form-0-slug": ".",
        }
        data.pop("form-0-name")
        request = rf_msg("post", "/admin/videos/~categories/", data)
        request.user = admin_user
        response = video_categories_view(request)
        assert response.status_code == 200
        assert "name" in response.context_data["formset"].errors[0]
        assert "slug" in response.context_data["formset"].errors[0]


class TestVideoPeopleListView:
    def test_get(self, admin_user: User, video_person: VideoPerson, rf: RequestFactory):
        request = rf.get("/admin/videos/~people/")
        request.user = admin_user
        request.resolver_match = resolve("/admin/videos/~people/")
        response = video_people_view(request)
        assert response.status_code == 200
        assert response.render()
        assert video_person.name in str(response.content)

    def test_update(
        self, admin_user: User, video_person: VideoPerson, rf_msg: RequestFactory
    ):
        data = {
            **CATEGORY_FORMSET_DATA,
            "form-0-id": video_person.id,
            "form-0-name": video_person.name,
            "form-0-slug": video_person.slug,
            "form-0-description": "X",
        }
        request = rf_msg("post", "/admin/videos/~people/", data)
        request.user = admin_user
        response = video_people_view(request)
        video_person.refresh_from_db()
        assert response.status_code == 302
        assert VideoPerson.objects.filter(slug="slug2").exists()
        assert video_person.description == "X"

    def test_fail_update(
        self, admin_user: User, video_person: VideoPerson, rf_msg: RequestFactory
    ):
        data = {
            **CATEGORY_FORMSET_DATA,
            "form-0-id": video_person.id,
            "form-0-slug": ".",
        }
        data.pop("form-0-name")
        request = rf_msg("post", "/admin/videos/~people/", data)
        request.user = admin_user
        response = video_people_view(request)
        assert response.status_code == 200
        assert "name" in response.context_data["formset"].errors[0]
        assert "slug" in response.context_data["formset"].errors[0]


class TestVideoKeywordListView:
    def test_get(
        self, admin_user: User, video_keyword: VideoKeyword, rf: RequestFactory
    ):
        request = rf.get("/admin/videos/~keywords/")
        request.resolver_match = resolve("/admin/videos/~keywords/")
        request.user = admin_user
        response = video_keywords_view(request)
        assert response.status_code == 200
        assert response.render()
        assert video_keyword.name in str(response.content)

    def test_update(
        self, admin_user: User, video_keyword: VideoKeyword, rf_msg: RequestFactory
    ):
        data = {
            **CATEGORY_FORMSET_DATA,
            "form-0-id": video_keyword.id,
            "form-0-name": video_keyword.name,
            "form-0-slug": video_keyword.slug,
            "form-0-description": "X",
        }
        request = rf_msg("post", "/admin/videos/~keywords/", data)
        request.user = admin_user
        response = video_keywords_view(request)
        video_keyword.refresh_from_db()
        assert response.status_code == 302
        assert VideoKeyword.objects.filter(slug="slug2").exists()
        assert video_keyword.description == "X"

    def test_fail_update(
        self, admin_user: User, video_keyword: VideoKeyword, rf_msg: RequestFactory
    ):
        data = {
            **CATEGORY_FORMSET_DATA,
            "form-0-id": video_keyword.id,
            "form-0-slug": ".",
        }
        data.pop("form-0-name")
        request = rf_msg("post", "/admin/videos/~keywords/", data)
        request.user = admin_user
        response = video_keywords_view(request)
        assert response.status_code == 200
        assert "name" in response.context_data["formset"].errors[0]
        assert "slug" in response.context_data["formset"].errors[0]
