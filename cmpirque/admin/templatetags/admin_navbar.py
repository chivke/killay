from django import template
from django.urls import reverse

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
        ("create", "Create Video", "videos:create"),
        ("categories", "Categories", "videos:categories"),
        ("people", "People", "videos:people"),
        ("keywords", "Keywords", "videos:keywords"),
    ]
    navbar_context = {
        "admin_conf": {
            "name": "Configuration",
            "link": reverse("admin:configuration"),
            "css_class": _get_css_class(view_name, "admin:configuration"),
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
    if view_name in [
        f"videos:{code}"
        for code in ["detail", "update", "sequences_list", "categorization"]
    ]:
        video_obj = context["object"]
        detail_video_admin_links = [
            ("public", video_obj.code, "videos:detail"),
            ("update", "Update", "videos:detail"),
            ("sequences_list", "Sequences", "videos:sequences_list"),
            ("categorization", "Categorization", "videos:categorization"),
        ]
        navbar_context["video_admin"]["selected"] = True
        for video_admin_link in detail_video_admin_links:
            navbar_context["video_admin"][video_admin_link[0]] = {
                "name": video_admin_link[1],
                "link": reverse(video_admin_link[2], kwargs={"slug": video_obj.code}),
                "css_class": _get_css_class(view_name, video_admin_link[2]),
            }
    return navbar_context
