from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from wagtail.images import get_image_model
from wagtail.images.models import SourceImageIOError
from wagtail.images.utils import verify_signature

from .backends import ImgProxyBackend


class RemoteRenditionServeView(View):
    model = get_image_model()
    # handle making this dynamic, including settings for particular backend
    backend_class = ImgProxyBackend
    key = None

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

        original_url = rendition.full_url
        remote_url = self.backend_class(original_url, filter_spec)()
        return redirect(remote_url)
