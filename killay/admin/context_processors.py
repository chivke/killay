from killay.admin.models import SiteConfiguration


def site_context(request):
    conf = SiteConfiguration.objects.current()
    return {"site_conf": conf}
