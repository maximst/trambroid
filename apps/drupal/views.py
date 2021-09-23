from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q

from .models import Forum

import os


def forum(request, path=None, slug=None):
    qs = Forum.objects.all()

    forum = None
    if slug:
        url = os.path.join(path, slug)

        try:
            forum = Forum.objects.get(url=url)
        except Forum.DoesNotExist:
            if slug.isdigit():
                forum = get_object_or_404(Forum, tid=slug)
            else:
                forum = get_object_or_404(Forum, url=url[:-1])

        qs = qs.filter(Q(parent=forum)|Q(parent__parent=forum))

    forums = qs.annotate(blogs_count=Count('blogs')).order_by('weight', '-name')

    context = {'parent_forum': forum, 'forums': forums}

    return render(request, 'forum.html', context)
