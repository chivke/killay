from django.urls import resolve
from killay.videos.models import VideoCollection


def collections_context(request):
    def _is_collection_selected(slug, resolve):
        return (resolve.kwargs.get("collection") or resolve.kwargs.get("slug")) == slug

    def _get_categories(collection, resolve):
        return [
            {
                "name": category.name,
                "slug": category.slug,
                "url": category.get_absolute_url(),
                "selected": category.slug == resolve.kwargs.get("slug"),
            }
            for category in collection.video_categories.all()
        ]

    resolve_from_path = resolve(request.path)
    collections = VideoCollection.objects.filter(is_visible=True)
    menu_collections = []
    for collection in collections:
        collection_item = {
            "name": collection.name,
            "slug": collection.slug,
            "url": collection.get_absolute_url(),
            "selected": _is_collection_selected(collection.slug, resolve_from_path),
            "categories": _get_categories(collection, resolve_from_path),
        }
        menu_collections.append(collection_item)
    return {"menu_collections": menu_collections}
