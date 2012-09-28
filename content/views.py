# -*-coding: utf8-*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from models import Blog

def blog_detail(request, slug):
    try:
        content = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Http404()
    contents = {'content': content}
    contents.update(csrf(request))
    return render_to_response('blog_detail.html', contents)


def blog_list(request):
    contents = Blog.objects.all()
    return render_to_response('blog_list.html', {'content': contents})
