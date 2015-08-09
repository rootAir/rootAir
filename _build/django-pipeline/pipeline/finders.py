from django.contrib.staticfiles.finders import BaseStorageFinder

from pipeline.storage import PipelineStorage


class PipelineFinder(BaseStorageFinder):
    storage = PipelineStorage
