from django.urls import path

from cmpirque.admin.views.configuration import admin_configuration_view

app_name = "admin"
urlpatterns = [path("", view=admin_configuration_view, name="configuration")]
