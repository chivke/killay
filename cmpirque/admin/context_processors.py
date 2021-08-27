from cmpirque.admin.models import AdminConfiguration


def site_context(request):
    conf = AdminConfiguration.objects.filter(active=True).first()
    return {"site_name": conf.site_name, "site_conf": conf}
