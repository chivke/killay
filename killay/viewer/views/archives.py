from killay.viewer.lib.constants import ViewerConstants, ViewerMessageConstants
from killay.viewer.engine.pipelines import ContentPipeline
from killay.viewer.views.mixins import ViewerViewBase


class ArchiveListView(ViewerViewBase):
    template_name = "viewer/archive-list.html"
    out_of_scope = [
        ViewerConstants.SCOPE_ONE_ARCHIVE,
        ViewerConstants.SCOPE_ONE_COLLECTION,
    ]

    def get_view_context_data(self, *args, **kwargs):
        self.pipeline = ContentPipeline(request=self.request)
        archives = self.pipeline.get_archives()
        archives_list_label = ViewerMessageConstants.LABEL_ARCHIVE_LIST.format(
            site=self.request.site_configuration.name
        )
        return {
            **ViewerMessageConstants.GENERAL_CONTEXT,
            "archive_list": archives,
            "archives_list_label": archives_list_label,
        }


archive_list_view = ArchiveListView.as_view()


class ArchiveDetailView(ViewerViewBase):
    template_name = "viewer/archive-detail.html"
    out_of_scope = [
        ViewerConstants.SCOPE_ONE_COLLECTION,
    ]

    def get_view_context_data(self, *args, **kwargs):
        pipeline = ContentPipeline(request=self.request)
        archive = pipeline.get_archive_by_slug()
        self.menu_cursor = {"archive": pipeline._archive_by_slug}
        return {
            **ViewerMessageConstants.GENERAL_CONTEXT,
            "archive_data": archive,
        }


archive_detail_view = ArchiveDetailView.as_view()
