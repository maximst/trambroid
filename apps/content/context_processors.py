from django.db.models import Count

from .models import Comment, Blog


def last_comments(request):
    lang = request.LANGUAGE_CODE

    comments = Comment.objects.select_related('blog').filter(
        blog__translations__language_code=lang,
        blog__is_active=True,
        is_active=True
    ).order_by('-create_time')[:10]
    return {'last_comments': comments}
