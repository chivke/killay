from tempfile import NamedTemporaryFile

from django.core.files import File

import pytest


@pytest.mark.django_db
class TestBulkActionListView:
    def test_get(self, admin_user, client):
        client.force_login(admin_user)
        response = client.get("/admin/cm/bulk-actions/")
        assert response.render()
        assert response.status_code == 200


@pytest.mark.django_db
class TestBulkActionView:
    def test_get(self, admin_user, client):
        client.force_login(admin_user)
        bulk_action_type = "piece_create"
        response = client.get(f"/admin/cm/bulk-actions/{bulk_action_type}/")
        assert response.render()
        assert response.status_code == 200

    def test_post_success(
        self, admin_user, client, bulk_action_piece_create_success_wb
    ):
        client.force_login(admin_user)
        bulk_action_type = "piece_create"
        with NamedTemporaryFile() as tmp_file:
            bulk_action_piece_create_success_wb.save(tmp_file.name)
            data = {"xls_file": File(tmp_file)}
            response = client.post(
                f"/admin/cm/bulk-actions/{bulk_action_type}/",
                data=data,
            )
        result = response.context["result"]
        assert result["is_valid"]
        assert result["data_success"][0]["code"]

    def test_post_data_error(
        self, admin_user, client, bulk_action_piece_create_success_wb
    ):
        client.force_login(admin_user)
        bulk_action_type = "piece_create"
        worksheet = bulk_action_piece_create_success_wb.active
        worksheet.cell(2, 1).value = None
        with NamedTemporaryFile() as tmp_file:
            bulk_action_piece_create_success_wb.save(tmp_file.name)
            data = {"xls_file": File(tmp_file)}
            response = client.post(
                f"/admin/cm/bulk-actions/{bulk_action_type}/",
                data=data,
            )
        result = response.context["result"]
        assert not result["is_valid"]
        assert result["data_errors"][0]

    def test_post_field_error(self, admin_user, client):
        client.force_login(admin_user)
        bulk_action_type = "piece_create"
        with NamedTemporaryFile() as tmp_file:
            data = {"xls_file": File(tmp_file)}
            response = client.post(
                f"/admin/cm/bulk-actions/{bulk_action_type}/",
                data=data,
            )
        result = response.context["result"]
        assert not result["is_valid"]
        assert result["data_errors"] is None
        assert result["file_errors"] == response.context["form"].errors["xls_file"]
