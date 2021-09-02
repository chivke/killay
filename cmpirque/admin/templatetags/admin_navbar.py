from django import template
from django.urls import reverse
from django.utils.translation import gettext_lazy

register = template.Library()


@register.inclusion_tag("components/admin_navbar.html", takes_context=True)
def show_admin_navbar(context):
    def _get_css_class(view, view_code):
        css_class = "item"
        if view == view_code:
            css_class += " active"
        return css_class

    request = context["request"]
    view_name = request.resolver_match.view_name
    video_admin_links = [
        ("create", gettext_lazy("Create Video"), "admin:videos_create"),
        ("categories", gettext_lazy("Categories"), "admin:videos_categories"),
        ("people", gettext_lazy("People"), "admin:videos_people"),
        ("keywords", gettext_lazy("Keywords"), "admin:videos_keywords"),
    ]
    navbar_context = {
        "admin_conf": {
            "name": gettext_lazy("Administrator"),
            "link": reverse("admin:configuration"),
            "css_class": "header " + _get_css_class(view_name, "admin:configuration"),
        },
        "user_conf": {
            "name": f"@{request.user.username}",
            "link": reverse("users:update"),
            "css_class": _get_css_class(view_name, "users:detail"),
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
        for code in ["update", "sequences_list", "categorization"]
    ]:
        video_obj = context["object"]
        detail_video_admin_links = [
            ("public", video_obj.code, "videos:detail"),
            ("update", gettext_lazy("Update"), "admin:videos_update"),
            ("delete", gettext_lazy("Delete"), "admin:videos_delete"),
            (
                "sequences_list",
                gettext_lazy("Sequences"),
                "admin:videos_sequences_list",
            ),
            (
                "categorization",
                gettext_lazy("Categorization"),
                "admin:videos_categorization",
            ),
        ]
        navbar_context["video_admin"]["selected"] = True
        for video_admin_link in detail_video_admin_links:
            navbar_context["video_admin"][video_admin_link[0]] = {
                "name": video_admin_link[1],
                "link": reverse(video_admin_link[2], kwargs={"slug": video_obj.code}),
                "css_class": _get_css_class(view_name, video_admin_link[2]),
            }
    return navbar_context
