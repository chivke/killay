from killay.admin.lib.constants import ContentManagerConstants


def get_content_manager_extra_links(view_slug: str) -> list:
    extra_links = []
    for slug in ContentManagerConstants.VIEW_SLUGS:
        if slug == view_slug:
            link = {"name": ContentManagerConstants.VIEWS_SECOND_TITLE[slug]}
        else:
            link = ContentManagerConstants.DICT_LINK[slug]["list"]
        extra_links.append(link)
    return extra_links
