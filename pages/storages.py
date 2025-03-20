from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class ImageLocalStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        location = location or os.path.join(settings.MEDIA_ROOT, 'images')
        base_url = base_url or os.path.join(settings.MEDIA_URL, 'images/')
        super().__init__(location, base_url)
