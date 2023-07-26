import pytest


from killay.archives.tests import recipes as archives_recipes
from killay.pages.tests.recipes import page_recipe
from killay.viewer.lib.constants import ViewerConstants


@pytest.mark.django_db
class TestRootView:
    root_path = "/viewer/"

    def test_default(self, client, user):
        client.force_login(user)
        response = client.get(self.root_path)
        assert response.url == f"{self.root_path}archives/"

    def test_default_with_one_archive(self, client, user, site_configuration):
        archive = archives_recipes.archive_recipe.make()
        site_configuration.viewer.scope = ViewerConstants.SCOPE_ONE_ARCHIVE
        site_configuration.viewer.scope_archive_id = archive.id
        site_configuration.viewer.save()
        client.force_login(user)
        response = client.get(self.root_path)
        assert response.url == f"{self.root_path}archives/{archive.slug}/"

    def test_default_with_one_collection(self, client, user, site_configuration):
        collection = archives_recipes.collection_recipe.make()
        site_configuration.viewer.scope = ViewerConstants.SCOPE_ONE_COLLECTION
        site_configuration.viewer.scope_collection_id = collection.id
        site_configuration.viewer.save()
        client.force_login(user)
        response = client.get(self.root_path)
        assert response.url == f"{self.root_path}pieces/"

    def test_with_home_page(self, client, user, site_configuration):
        page = page_recipe.make()
        site_configuration.viewer.home = ViewerConstants.HOME_PAGE
        site_configuration.viewer.home_page_id = page.id
        site_configuration.viewer.save()
        client.force_login(user)
        response = client.get(self.root_path)
        assert response.url == f"/pages/{page.slug}/"
