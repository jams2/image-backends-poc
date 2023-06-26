import logging

from django.core import cache
from django import template

from wagtail.images.views.serve import generate_image_url

from home.backends import ImgProxyBackend, construct_cache_key

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag()
def image_url(image, filter_spec, viewname="imgproxy_serve"):
    cache_key = construct_cache_key(image, filter_spec, ImgProxyBackend)
    if (cached := cache.caches["renditions"].get(cache_key)) is not None:
        logger.debug("Cache hit with key %s", cache_key)
        return cached

    logger.debug("Cache miss with key %s", cache_key)
    return generate_image_url(image, filter_spec, viewname)
