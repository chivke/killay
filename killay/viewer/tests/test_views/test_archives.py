import pytest


from killay.archives.tests import recipes as archives_recipes
from killay.viewer.lib.constants import ViewerConstants


@pytest.mark.django_db
class TestArchiveList:
    path = "/archives/"

    def test_response(self, client, site_configuration):
        assert site_configuration.viewer.scope == ViewerConstants.SCOPE_ALL
        archive = archives_recipes.archive_recipe.make()
        response = client.get(self.path)
        assert response.status_code == 200
        assert response.context["archive_list"][0]["slug"] == archive.slug

    def test_out_of_scope(self, client, site_configuration):
        archive = archives_recipes.archive_recipe.make()
        site_configuration.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        site_configuration.viewer.scope_archive_id = archive.id
        site_configuration.viewer.save()
        response = client.get(self.path)
        assert response.status_code == 302
        assert response.url == f"{self.path}{archive.slug}/"


@pytest.mark.django_db
class TestArchiveDetailView:
    path = "/archives/{slug}/"

    def test_response(self, client, site_configuration):
        assert site_configuration.viewer.scope == ViewerConstants.SCOPE_ALL
        archive = archives_recipes.archive_recipe.make()
        response = client.get(self.path.format(slug=archive.slug))
        assert response.status_code == 200
        assert response.context["archive_data"]["slug"] == archive.slug

    def test_out_of_scope(self, client, site_configuration):
        collection = archives_recipes.collection_recipe.make()
        site_configuration.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        site_configuration.viewer.scope_collection_id = collection.id
        site_configuration.viewer.save()

        response = client.get(self.path.format(slug=collection.archive.slug))
        assert response.status_code == 302
        assert response.url == "/pieces/"
