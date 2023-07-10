from django.core import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from wagtail.images import get_image_model
from wagtail.images.models import SourceImageIOError
from wagtail.images.utils import verify_signature

from .backends import construct_cache_key


class RemoteRenditionServeView(View):
    model = get_image_model()
    backend_class = None
    key = None

    def __init__(self, backend_class, *args, **kwargs):
        self.backend_class = backend_class
        super().__init__(*args, **kwargs)

    def get(self, request, signature, image_id, filter_spec):
        if not verify_signature(
            signature.encode(), image_id, filter_spec, key=self.key
        ):
            raise PermissionDenied

        image = get_object_or_404(self.model, id=image_id)
        try:
            rendition = image.get_rendition("original")
        except SourceImageIOError:
            return HttpResponse(
                "Source image file not found", content_type="text/plain", status=410
            )

        original_url = f"{self.backend_class.get_original_rendition_url_prefix()}{rendition.url}"
        remote_url = self.backend_class(original_url, filter_spec)()
        cache_key = construct_cache_key(image, filter_spec, self.backend_class)

        # Cached URL may accessed from home_tags.image_url, saving a request per-image
        cache.caches["renditions"].set(cache_key, remote_url)
        return redirect(remote_url)
