from django.urls import resolve
from django.conf import settings

from cmpirque.pages.models import Page


def site_context(request):
    return {"site_name": settings.SITE_NAME}


def pages_context(request):
    resolve_from_path = resolve(request.path)
    selected_map = {"home": True if resolve_from_path.url_name == "home" else False}
    if (
        resolve_from_path.view_name == "page:detail"
        and "slug" in resolve_from_path.kwargs
    ):
        selected_map[resolve_from_path.kwargs["slug"]] = True
    return {
        "menu_pages": [
            {
                "title": page.title,
                "slug": page.slug,
                "url": page.get_absolute_url(),
                "selected": selected_map.get(page.slug, False)
            }
            for page in Page.objects.all()
        ]
    }
