from django import template
from django.urls import reverse
from django.utils.translation import gettext_lazy

register = template.Library()


@register.inclusion_tag("admin/components/navbar.html", takes_context=True)
def show_admin_navbar(context):
    def _get_css_class(view, view_code):
        css_class = "item"
        if (isinstance(view_code, list) and view in view_code) or (
            isinstance(view_code, str) and view == view_code
        ):
            css_class += " active"
        return css_class

    request = context["request"]
    view_name = request.resolver_match.view_name
    video_admin_links = [
        ("create", gettext_lazy("Create Video"), "admin:videos_create"),
        ("collections", gettext_lazy("Collections"), "admin:videos_collections"),
        ("categories", gettext_lazy("Categories"), "admin:videos_categories"),
        ("people", gettext_lazy("People"), "admin:videos_people"),
        ("keywords", gettext_lazy("Keywords"), "admin:videos_keywords"),
    ]
    navbar_context = {
        "admin_conf": {
            "name": gettext_lazy("Administrator"),
            "link": reverse("admin:site_configuration"),
            "css_class": "header "
            + _get_css_class(view_name, "admin:site_configuration"),
        },
        "video_admin": {
            video_admin_link[0]: {
                "name": video_admin_link[1],
                "link": reverse(video_admin_link[2]),
                "css_class": _get_css_class(view_name, video_admin_link[2]),
            }
            for video_admin_link in video_admin_links
        },
    }
    if view_name in ["videos:detail"] + [
        f"admin:videos_{code}"
        for code in [
            "update",
            "delete",
            "sequences_list",
            "sequences_create",
            "categorization",
        ]
    ]:
        video_obj = context["object"]
        collection = video_obj.categorization.collection
        detail_video_admin_links = [
            ("public", video_obj.code, "videos:detail"),
            ("update", gettext_lazy("Update"), "admin:videos_update"),
            ("delete", gettext_lazy("Delete"), "admin:videos_delete"),
            (
                "sequences_list",
                gettext_lazy("Sequences"),
                ["admin:videos_sequences_list", "admin:videos_sequences_create"],
            ),
            (
                "categorization",
                gettext_lazy("Categorization"),
                "admin:videos_categorization",
            ),
        ]
        navbar_context["video_admin"]["selected"] = True
        for video_admin_link in detail_video_admin_links:
            reverse_link = video_admin_link[2]
            if isinstance(reverse_link, list):
                reverse_link = reverse_link[0]
            navbar_context["video_admin"][video_admin_link[0]] = {
                "name": video_admin_link[1],
                "link": reverse(
                    reverse_link,
                    kwargs={"slug": video_obj.code, "collection": collection.slug},
                ),
                "css_class": _get_css_class(view_name, video_admin_link[2]),
                "selected": True,
            }
    return navbar_context
