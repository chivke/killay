def site_context(request):
    conf = request.site_configuration
    return {"site_conf": conf, "ip_address": request.ip_address}
