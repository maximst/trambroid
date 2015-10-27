from .models import Comment, Blog

from django.db.models import Count
from hvad.utils import get_translation_aware_manager

def last_comments(request):
    lang = request.LANGUAGE_CODE

    comments = get_translation_aware_manager(Comment).language(lang)\
            .select_related('blog').filter(blog__language_code=lang,
            blog__is_active=True, is_active=True).order_by('-create_time')[:10]
    return {'last_comments': comments}