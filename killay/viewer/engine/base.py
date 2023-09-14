from typing import Dict, Optional

from django.http import HttpRequest
from django.urls import reverse

from killay.viewer.lib.constants import ViewerConstants, ViewerPatternConstants


class PipelineBase:
    def __init__(
        self,
        request: HttpRequest,
        cursor: Optional[Dict] = None,
    ) -> None:
        self.request = request
        self.cursor = cursor or {}
        self.conf = request.site_configuration
        self.viewer = request.viewer
        self.user = request.user
        self.place = request.place
        self.init_prepare()

    def init_prepare(self) -> None:
        pass

    def _can_access(self):
        return self.conf.is_published or self.user.is_superuser

    @staticmethod
    def _get_piece_list_base_url() -> str:
        pattern = ViewerPatternConstants.pattern_by_name(
            name=ViewerPatternConstants.PIECE_LIST
        )
        base_url = reverse(pattern)
        return base_url

    def _get_url_param(self, key: str) -> Optional[str]:
        value = self.request.GET.get(key, "").strip()
        return value or None

    def get_queryparams(self) -> str:
        queryparams_list = [
            f"{key}={value}"
            for key, value in self.request.GET.items()
            if key in ViewerConstants.CURSOR_KEYS
        ]
        return "&".join(queryparams_list)
