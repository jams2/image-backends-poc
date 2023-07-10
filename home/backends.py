from django.conf import settings
import imgix
import imgproxy


def construct_cache_key(image, filter_spec, backend):
    return f"{backend.cache_key}-{image.id}-{filter_spec}"


class BaseImageProcessingBackend:
    cache_key = ""

    def __init__(self, source_url, filter_spec):
        self.source_url = source_url
        self.filter_spec = filter_spec
        self.kwargs = self.parse(filter_spec)

    def parse(self, filter_spec):
        raise NotImplementedError

    def get_url(self):
        raise NotImplementedError

    @staticmethod
    def get_original_rendition_url_prefix():
        return ""

    def __call__(self):
        return self.get_url()


class ImgProxyBackend(BaseImageProcessingBackend):
    cache_key = "imgproxy"
    operation_mappings = {
        "resize": "resizing_type",
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
                    kwargs[self.operation_mappings.get(param, param)] = arg
                except ValueError:
                    kwargs["advanced"].append(directive)
        return kwargs


class ImgixBackend(BaseImageProcessingBackend):
    operation_mappings = {
        "height": "h",
        "width": "w",
        "resize": "fit",
    }

    @staticmethod
    def get_original_rendition_url_prefix():
        return settings.PROXY_URL_FOR_IMGIX

    def get_url(self):
        builder = imgix.UrlBuilder(
            settings.IMGIX_DOMAIN, sign_key=settings.IMGIX_SIGNATURE_KEY
        )
        return builder.create_url(self.source_url, self.kwargs)

    def parse(self, filter_spec):
        # Only width, height, and resize mode have been tested
        kwargs = {}
        for directive in filter_spec.split("|"):
            if directive == "enlarge":
                kwargs["enlarge"] = True
            else:
                param, arg = directive.split("-")
                kwargs[self.operation_mappings.get(param, param)] = arg
        return kwargs
