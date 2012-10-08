#-*-coding: utf8-*-
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from voting.models import Vote


def homepage(request):
    model = ContentType.objects.get(app_label='content',
                                    model=settings.DISPLAY_CONTENT_TYPES[0])
    return None

@login_required
def vote(request, app, model, pk, vote):
    redirect_url = request.META.get('HTTP_REFERER')
    user = request.user

    try:
        content_type = ContentType.objects.get(app_label=app, model=model)
    except ContentType.DoesNotExist:
        raise Http404()

    try:
        content_model = content_type.model_class()
        obj = content_model.objects.get(pk=pk)
    except content_model.DoesNotExist:
        raise Http404()

    Vote.objects.record_vote(obj, user, int(vote))

    if not redirect_url:
        try:
            redirect_url = reverse(model, kwargs={'slug': obj.slug})
        except:
            redirect_url = '/'

    return redirect(redirect_url)
