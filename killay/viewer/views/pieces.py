from typing import Dict, Optional

from django.http import Http404
from django.views.generic.list import MultipleObjectMixin

from killay.archives.lib.constants import PieceConstants
from killay.viewer.engine.pipelines import ContentPipeline
from killay.viewer.lib.constants import ViewerMessageConstants, ContentConstants
from killay.viewer.views.mixins import ViewerViewBase


class PieceListView(ViewerViewBase, MultipleObjectMixin):
    template_name = "viewer/piece-list.html"
    paginate_by = 54

    def get_view_context_data(self):
        search = self._get_search()
        specific_context = self._get_specific_context()
        return {
            "archive": self.archive,
            "collection": self.collection,
            "category": self.category,
            "query_search": self.query_search,
            "search": search,
            "specific_context": specific_context,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        paginator = context["paginator"]
        page_obj = context["page_obj"]
        context["total_founded"] = ViewerMessageConstants.TOTAL_FOUNDED_PIECES.format(
            number=len(self.object_list)
        )
        context["pagination"] = self._get_pagination(
            paginator=paginator,
            page_obj=page_obj,
            queryparams=self.query_params,
        )
        return context

    def fetch_data(self) -> None:
        pipeline = ContentPipeline(request=self.request)
        self.collection = pipeline.get_collection()
        self.category = (
            pipeline.get_category(collection_id=self.collection.id)
            if self.collection
            else None
        )
        self.person = pipeline.get_person()
        self.keyword = pipeline.get_keyword()
        self.archive = pipeline.get_archive(
            collection=self.collection,
            category=self.category,
        )
        self.object_list = pipeline.get_pieces(
            archive=self.archive,
            collection=self.collection,
            category=self.category,
        )
        self.filter_options = pipeline.get_filter_options(
            archive=self.archive,
            collection=self.collection,
            category=self.category,
        )
        self.kind_options = pipeline.get_kind_options()
        self.menu_cursor = {
            "archive": self.archive,
            "collection": self.collection,
            "category": self.category,
            "person": self.person,
            "keyword": self.keyword,
        }
        self.query_search = pipeline.get_query_search()
        self.query_params = pipeline.get_queryparams()

    def _get_specific_context(self) -> Optional[Dict]:
        if self.query_search:
            return
        if not self.person and self.keyword:
            instance = self.keyword
            label = ContentConstants.LABEL_KEYWORD
        elif not self.keyword and self.person:
            instance = self.person
            label = ContentConstants.LABEL_PERSON
        elif not self.keyword and not self.person and self.category:
            instance = self.category
            label = None
        else:
            return
        return {
            "title": instance.name,
            "content": instance.description,
            "label": label,
        }

    def _get_search(self) -> Dict:
        applied_filters = 0
        for option in self.filter_options.values():
            applied_filters += sum([1 for item in option["items"] if item["active"]])
        applied_filters += sum(
            [1 for item in self.kind_options["items"] if item["active"]]
        )
        applied_filters_message = ViewerMessageConstants.SEARCH_APPLIED_FILTERS.format(
            applied_filters=applied_filters
        )
        return {
            "query": self.query_search,
            "applied_filters_message": applied_filters_message,
            "filter_options": self.filter_options,
            "kind_options": self.kind_options,
            "label_name": ViewerMessageConstants.SEARCH_TOOL_NAME,
            "action_name": ViewerMessageConstants.SEARCH_ACTION_NAME,
        }

    def _get_pagination(self, paginator, page_obj, queryparams):
        queryparams = f"&{queryparams}" if queryparams else ""
        template = "?page={number}{qp}"
        page_links = self._get_init_pages(
            template=template, queryparams=queryparams, page_obj=page_obj
        )
        total = paginator.num_pages
        current_index = page_obj.number - 1
        init = current_index - 3
        if init < 0:
            end = current_index + 3 + abs(init)
            init = 0
        else:
            end = current_index + 3
        if total < end:
            diff = init - (end - total)
            if diff < 0:
                diff = 0
            init = diff
        for index in range(paginator.num_pages)[init:end]:
            page_number = index + 1
            page_link = {
                "number": page_number,
                "link": template.format(number=page_number, qp=queryparams),
                "disabled": page_number == page_obj.number,
            }
            page_links.append(page_link)
        page_links.extend(
            self._get_end_pages(
                template=template,
                queryparams=queryparams,
                page_obj=page_obj,
                paginator=paginator,
            )
        )
        return page_links

    def _get_init_pages(self, template, queryparams, page_obj):
        first_page = {
            "number": "first",
            "link": template.format(number=1, qp=queryparams),
            "disabled": page_obj.number == 1,
        }
        previous_page = {
            "number": "previous",
            "link": (
                template.format(number=page_obj.previous_page_number(), qp=queryparams)
                if page_obj.has_previous()
                else None
            ),
            "disabled": not page_obj.has_previous(),
        }
        return [first_page, previous_page]

    def _get_end_pages(self, template, queryparams, page_obj, paginator):
        next_page = {
            "number": "next",
            "link": (
                template.format(number=page_obj.next_page_number(), qp=queryparams)
                if page_obj.has_next()
                else None
            ),
            "disabled": not page_obj.has_next(),
        }
        last_page = {
            "number": "last",
            "link": template.format(number=paginator.num_pages, qp=queryparams),
            "disabled": page_obj.number == paginator.num_pages,
        }
        return [next_page, last_page]


piece_list_view = PieceListView.as_view()


class PieceDetailView(ViewerViewBase):
    template_name = "viewer/piece-detail.html"
    kind_key_map = {
        PieceConstants.KIND_VIDEO: "videos",
        PieceConstants.KIND_IMAGE: "images",
        PieceConstants.KIND_SOUND: "sounds",
        PieceConstants.KIND_DOCUMENT: "documents",
    }

    def fetch_data(self) -> None:
        piece_code = self.kwargs.get("slug")
        pipeline = ContentPipeline(request=self.request)
        piece_data = pipeline.get_piece(piece_code=piece_code) if piece_code else None
        if not piece_data:
            raise Http404(ViewerMessageConstants.PIECE_NOT_FOUND)
        self.piece_data = piece_data
        piece = piece_data["instance"]
        self.menu_cursor = {
            "archive": piece.collection.archive,
            "collection": piece.collection,
            "category": piece.categories.first(),
            "piece": piece,
        }

    def get_view_context_data(self):
        player_template = self._get_template_player(kind=self.piece_data["kind"])
        return {
            "piece": self.piece_data,
            "player_template": player_template,
        }

    def _get_template_player(self, kind: str) -> str:
        kind_key = self.kind_key_map.get(kind)
        return f"viewer/components/{kind_key}/player.html"


piece_detail_view = PieceDetailView.as_view()
