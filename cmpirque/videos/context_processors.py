from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy

from cmpirque.videos.models import VideoCategory


def categories_context(request):
    resolve_from_path = resolve(request.path)
    selected_map = {}
    if (
        resolve_from_path.view_name == "videos:category-list"
        and "slug" in resolve_from_path.kwargs
    ):
        selected_map[resolve_from_path.kwargs["slug"]] = True
    return {
        "menu_categories": [
            {
                "name": category.name,
                "slug": category.slug,
                "url": category.get_absolute_url(),
                "selected": selected_map.get(category.slug, False),
            }
            for category in VideoCategory.objects.all()
        ]
        + [
            {
                "name": gettext_lazy("All"),
                "url": reverse("videos:list"),
                "selected": True
                if resolve_from_path.view_name == "videos:list"
                else False,
            }
        ]
    }
