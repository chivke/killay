from unittest import mock

import pytest


from killay.viewer.engine.base import PipelineBase


@pytest.mark.django_db
class TestPipelineBase:
    @mock.patch("killay.viewer.engine.base.PipelineBase.init_prepare")
    def test_init_prepare(self, init_prepare, get_request_with_viewer):
        request = get_request_with_viewer()
        PipelineBase(request=request)
        assert init_prepare.called

    def test_can_access(self, get_request_with_viewer):
        request = get_request_with_viewer()
        pipeline = PipelineBase(request=request)
        assert pipeline._can_access()

    def test_get_piece_list_base_url(self, get_request_with_viewer):
        request = get_request_with_viewer()
        pipeline = PipelineBase(request=request)
        assert pipeline._get_piece_list_base_url() == "/viewer/pieces/"

    def test_get_url_param(self, get_request_with_viewer):
        fake_key = "fake"
        fake_content = "active"
        request = get_request_with_viewer(f"/?{fake_key}={fake_content}")
        pipeline = PipelineBase(request=request)
        assert pipeline._get_url_param(key=fake_key) == fake_content

    def test_get_queryparams(self, get_request_with_viewer):
        fake_key = "search"
        fake_content = "active"
        query_params = f"{fake_key}={fake_content}"
        request = get_request_with_viewer(f"/?{query_params}")
        pipeline = PipelineBase(request=request)
        assert pipeline.get_queryparams() == query_params
