from django.conf import settings
import imgproxy


class BaseImageProcessingBackend:
    def __init__(self, source_url, filter_spec):
        self.source_url = source_url
        self.filter_spec = filter_spec
        self.kwargs = self.parse(filter_spec)

    def parse(self, filter_spec):
        raise NotImplementedError

    def get_url(self):
        raise NotImplementedError

    def __call__(self):
        return self.get_url()


class ImgProxyBackend(BaseImageProcessingBackend):
    operation_mappings = {
        "resize": "resizing_type",
        "width": "width",
        "height": "height",
        "gravity": "gravity",
        "enlarge": "enlarge",
        "extension": "extension",
    }

    def get_url(self):
        imgproxy_url = imgproxy.ImgProxy(
            image_url=self.source_url,
            proxy_host=settings.IMGPROXY_HOST,
            key=settings.IMGPROXY_KEY,
            salt=settings.IMGPROXY_SALT,
            **self.kwargs,
        )
        return imgproxy_url()

    def parse(self, filter_spec):
        kwargs = {"advanced": []}
        for directive in filter_spec.split("|"):
            if directive == "enlarge":
                kwargs["enlarge"] = True
            else:
                try:
                    param, arg = directive.split("-")
                    kwargs[self.operation_mappings[param]] = arg
                except (ValueError, KeyError):
                    kwargs["advanced"].append(directive)
        return kwargs
