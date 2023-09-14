from django.http import HttpRequest


from killay.viewer.engine.pipelines import SiteContextPipeline


META = {"author": "chivke"}


def general_context(request: HttpRequest):
    pipeline = SiteContextPipeline(request=request)
    site_context = pipeline.get_site_context()
    return {
        "meta": META,
        "site": site_context,
    }
