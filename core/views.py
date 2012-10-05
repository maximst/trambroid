#-*-coding: utf8-*-
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


def homepage(request):
    model = ContentType.objects.get(app_label='content',
                                    model=settings.DISPLAY_CONTENT_TYPES[0])
    return None
