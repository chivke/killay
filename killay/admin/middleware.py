from killay.admin.services import get_site_configuration
from killay.archives.services import get_place_from_ip_address


class SiteConfigurationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.site_configuration = get_site_configuration()
        ip_address = self._get_ip_address(request=request)
        request.ip_address = ip_address
        request.place = get_place_from_ip_address(ip_address=ip_address)
        response = self.get_response(request)
        return response

    @staticmethod
    def _get_ip_address(request) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")
        return ip_address
