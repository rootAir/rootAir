import os

from django.core.cache import cache
from django.dispatch import Signal, receiver

from pipeline.conf import settings


css_compressed = Signal(providing_args=["package", "version"])
js_compressed = Signal(providing_args=["package", "version"])


@receiver(css_compressed)
@receiver(js_compressed)
def invalidate_cache(sender, package, version, **kwargs):
    filename_base, filename = os.path.split(package['output'])
    cache.set("pipeline:%s" % filename, str(version),
            settings.PIPELINE_CACHE_TIMEOUT)
