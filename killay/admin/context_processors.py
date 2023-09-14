from killay.admin.engine.navbar import AdminNavContext


def site_context(request):
    conf = request.site_configuration
    context = {"site_conf": conf, "ip_address": request.ip_address}
    if request.user.is_superuser:
        context["admin_nav"] = AdminNavContext(request=request).get()
    return context
