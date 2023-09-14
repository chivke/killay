from django.views.generic import RedirectView

from killay.viewer.engine.pipelines import RoutePipeline


class RootView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return RoutePipeline.get_root_url(request=self.request)


root_view = RootView.as_view()
